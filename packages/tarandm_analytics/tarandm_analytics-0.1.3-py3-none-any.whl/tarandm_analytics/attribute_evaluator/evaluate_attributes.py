from datetime import datetime
from uuid import UUID

import requests
import structlog
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

from tarandm_analytics.base_class import TaranDMAnalytics

logger = structlog.get_logger(__name__)


class EvaluateAttributes(TaranDMAnalytics):
    def __init__(self, endpoint_url: Optional[str], username: Optional[str], password: Optional[str]):
        super().__init__(endpoint_url=endpoint_url, username=username, password=password)
        self.authorization: HTTPBasicAuth = HTTPBasicAuth(self.username, self.password)
        self.last_attribute_extractor_id: Optional[Dict[{str, Union[str, datetime]}]] = None
        self.attribute_extractor_ids: List[Dict[{str, Union[str, datetime]}]] = []

    def check_evaluation_progress(self, attribute_extractor_id: Optional[str] = None) -> str:
        if attribute_extractor_id is None:
            if self.last_attribute_extractor_id is None:
                return "Attribute extraction was not triggered yet. You can also provide attribute_extractor_id as a " \
                       "parameter to extract data from past extraction process."
            attribute_extractor_id = self.last_attribute_extractor_id['id']

        url = self.endpoint_url + "analytics/check_attributes_evaluator_progress"
        request_data = {
            "process_id": attribute_extractor_id
        }

        response = requests.post(url=url, params=request_data, auth=self.authorization)
        if response.status_code == 200:
            logger.info("Attribute evaluation progress status checked.")

        return response.json()["status"]

    def evaluate(
        self,
        attribute_classes: List[str],
        input_data_class: str,
        business_case: str,
        repository: str,
        git_user_name: str,
        git_user_email: str,
        git_user_token: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        decision_ids: Optional[List[str]] = None,
        orig_git_branch: Optional[str] = "develop-simulation",
    ) -> None:
        url = self.endpoint_url + "analytics/attributes_evaluator"

        date_from = date_from or "1900-01-01"
        date_to = date_to or "2100-12-31"

        request_data = {
            "date_from": date_from,
            "date_to": date_to,
            "decision_ids": [UUID(did) for did in decision_ids] if decision_ids is not None else None,
            "attribute_classes": attribute_classes,
            "input_data_class": input_data_class,
            "business_case": business_case,
        }

        repository_config = {
            "class": "tarandm_utils.model.repository_config.project.ProjectRepositoryConfig",
            "class_version": "a492a7ba",
            "readonly": "false",
            "source": "Attribute evaluator",
            "customer_version": "local",
            "repository": repository,
            "branch": f"{orig_git_branch}-attribute-evaluator",
            "original_branch": orig_git_branch,
            "user_name": git_user_name,
            "user_email": git_user_email,
            "user_token": git_user_token,
        }

        headers = {"tarandm-repository_config": str(repository_config).replace("'", '"')}

        response = requests.post(url=url, params=request_data, headers=headers, auth=self.authorization)

        if response.status_code == 200:
            logger.info("Attributes were evaluated and stored to DB.")
        else:
            logger.error(f"Was not able to evaluate attributes. Status code {response.status_code}.")

        self.last_attribute_extractor_id = {"id": response.json().get("impact_report_id"), "created": datetime.now()}
        self.attribute_extractor_ids.append(self.last_attribute_extractor_id)

    def get_attribute_classes(self) -> Optional[Dict[str, List[str]]]:
        url = self.endpoint_url + "strategies/attribute_classes"

        response = requests.post(url=url, auth=self.authorization)

        if response.status_code != 200:
            logger.error(f"Failed to fetch list of attribute classes: {response.status_code}")
            return None

        result = {}
        for attr_class_source, attr_classes in response.json().items():
            for attr_class in attr_classes:
                result[attr_class["class_name"]] = list(attr_class["attributes"].keys())

        return result

    def get_business_cases(self, selector_name: str = "demo") -> Optional[Dict[str, Dict[str, str]]]:
        url = self.endpoint_url + "strategies/selectors"

        response = requests.post(
            url=url, json={"action": "get", "params": {"name": selector_name}}, auth=self.authorization
        )

        if response.status_code != 200:
            logger.error(f"Failed to fetch list of attribute classes: {response.status_code}")
            return None

        result = {}
        for business_case in response.json()["business_cases"]:
            result[business_case["name"]] = {
                "input_class": business_case["input_class"],
                "audiences": [audience["query"] for audience in business_case["audiences"]],
            }

        return result

    def generate_query_to_extract_attributes(self, db_id: Optional[str] = None) -> str:
        if db_id is None:
            db_id = self.last_attribute_extractor_id["id"]

        query = f"""
            SELECT
                t.decision_id,
                jsonb_object_agg(sub_key, sub_value) AS extracted_attributes
            FROM
                (
                    SELECT
                        ds.original_decision_id AS decision_id,
                        (jsonb_each(dib."content"::jsonb)).key AS sub_key,
                        (jsonb_each(dib."content"::jsonb)).value AS sub_value
                    FROM
                        decision_impact_report 			AS dir
                        INNER JOIN
                        decision_simulation 			AS ds  ON ds.decision_id = dir.decision_id 
                        INNER JOIN
                        decision_iteration 				AS di  ON di.decision_id = dir.decision_id
                        INNER JOIN
                        decision_iteration_blockdata 	AS dib ON dib.iteration_id = di.iteration_id
                    WHERE dir.impact_report_id = '{db_id}'
                ) AS t
            GROUP BY t.decision_id
        """

        return query

    def fetch_data_from_db(
        self,
        attribute_extractor_id: Optional[str] = None
    ) -> Optional["pd.DataFrame"]:
        status = self.check_evaluation_progress()

        if status == 'RUNNING':
            logger.info("Attribute evaluation still running.")
            return None
        elif status != 'FINISHED':
            logger.warning(f"Attribute evaluation status: {status}.")
            return None

        logger.info("Attribute evaluation finished. Data fetching stated.")

        if attribute_extractor_id is None:
            if self.last_attribute_extractor_id is None:
                logger.info("Attribute extraction was not triggered yet. You can also provide attribute_extractor_id "
                            "as a parameter to extract data from past extraction process.")
                return None
            attribute_extractor_id = self.last_attribute_extractor_id["id"]

        url = self.endpoint_url + "analytics/get_attributes_evaluator_data"
        request_data = {
            "process_id": attribute_extractor_id
        }

        response = requests.post(url=url, params=request_data, auth=self.authorization)
        if response.status_code == 200:
            logger.info("Attribute evaluation progress status checked.")

        import pandas as pd

        df = pd.DataFrame()
        for decision_id, db_row in response.json().items():
            pd_row = {
                "decision_id": decision_id,
            }

            attrs = db_row
            for attr_name, val in attrs.items():
                if isinstance(val, dict) and "amount" in val.keys():
                    amount = val.get("amount")
                    currency = val.get("currency", "")
                    attrs[attr_name] = f"{amount}{currency}"
            pd_row.update(attrs)

            df = pd.concat([df, pd.DataFrame(pd.Series(pd_row)).T])

        return df
