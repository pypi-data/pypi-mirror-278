import os
from .api_client import APIClientBase, InvalidInputException
from typing import List, Dict


class Protection(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(url_base or os.environ.get("PROTECTION_SERVICE", ""), **kwargs)

    def get_policies(self):
        return self.get_request("/policies")

    def get_policy(self, id):
        if not id:
            raise InvalidInputException(f"Expected a valid policy id, received: `{id}`")
        return self.get_request("/policies/{id}", id=id)

    def create_policy(self, policy_name: str, pool_name: str = None, alert_enabled: bool = True, rules: list = None):
        body = {
            "policyName": policy_name,
            "poolName": pool_name,
            "alertEnabled": alert_enabled,
            "rules": rules or [],
        }
        return self.post_request("/policies", body=body)

    def patch_policy(
        self, id: str, policy_name: str = None, pool_name: str = None, alert_enabled: bool = None, rules: list = None
    ):
        if not id:
            raise InvalidInputException(f"Expected a valid policy id, received: `{id}`")
        body = {}

        if policy_name is not None:
            body["policyName"] = policy_name
        if pool_name is not None:
            body["poolName"] = pool_name
        if alert_enabled is not None:
            body["alertEnabled"] = alert_enabled
        if rules is not None:
            body["rules"] = rules

        return self.patch_request("/policies/{id}", id=id, body=body)

    def delete_policy(self, id):
        if not id:
            raise InvalidInputException(f"Expected a valid policy id, received: `{id}`")
        return self.get_request("/policies/{id}", id=id)

    def get_replication_hosts(self):
        return self.get_request("/hosts")

    def get_replication_host(self, id):
        if not id:
            raise InvalidInputException(f"Expected a valid host id, received: `{id}`")
        return self.get_request("/hosts/{id}", id=id)

    def create_replication_host(self, body):
        return self.post_request("/hosts", body=body)

    def delete_replication_host(self, id):
        if not id:
            raise InvalidInputException(f"Expected a valid host id, received: `{id}`")
        return self.delete_request("/hosts/{id}", id=id)

    def patch_replication_host(self, id, body):
        if not id:
            raise InvalidInputException(f"Expected a valid host id, received: `{id}`")
        return self.patch_request("/hosts/{id}", id=id, body=body)

    def get_protected_vms(self):
        return self.get_request("/vms")

    def get_protected_vm(self, vm_syn_id: str):
        if not vm_syn_id:
            raise InvalidInputException(f"Expected a valid protected VM id, received: `{vm_syn_id}`")
        return self.get_request("/vms/{vm_syn_id}", vm_syn_id=vm_syn_id)

    def post_vm_recovery_point(self, vm_syn_id: str, job_id: str):
        return self.post_request("/vms/recovery-points", body={"synId": vm_syn_id, "jobId": job_id})

    def get_recovery_points(self, vm_syn_id: str, limit: int = 100, offset: int = 0, triggers: list = None):
        """
        Retrieves recovery points for a virtual machine identified by its ID.

        Args:
            vm_syn_id (str): The virtual machine identifier.
            limit (int, optional): The maximum number of recovery points to retrieve. Defaults to 100.
            offset (int, optional): The offset for pagination. Defaults to 0.
            triggers (list, optional): A list of recovery point triggers to filter the results. Defaults to None.

        Returns:
            dict: A list of dictionaries representing the recovery points.

        Raises:
            APIException: If the request fails for any reason.

        Example:
            >>> recovery_points = protection_api.get_recovery_points(vm_syn_id="example_id", limit=50, offset=0, triggers=["scheduled", "manual"])
        """
        # We use a list of tuples instead of a dict because we can have type=foo&type=bar (i.e. same key multiple times)
        query_args = [("vmSynId", vm_syn_id), ("limit", limit), ("offset", offset)]
        if triggers:
            for t in triggers:
                query_args.append(("triggers", t))
        return self.get_request("/recovery-points", query_args=query_args)

    def get_recovery_point(self, recovery_point_id: str):
        if not recovery_point_id:
            raise InvalidInputException(f"Expected a valid recovery point id, received: `{recovery_point_id}`")
        return self.get_request(f"/recovery-points/{recovery_point_id}")

    def delete_recovery_point(self, recovery_point_id: str):
        if not recovery_point_id:
            raise InvalidInputException(f"Expected a valid recovery point id, received: `{recovery_point_id}`")
        return self.delete_request(f"/recovery-points/{recovery_point_id}")

    def patch_recovery_point(self, recovery_point_id: str, body: Dict):
        """
        Patch a recovery point identified by its ID with the provided data.

        Parameters:
        - recovery_point_id (str): The ID of the recovery point to be patched.
        - body (Dict): A dictionary containing the data to be updated for the recovery point.

        Raises:
        - InvalidInputException: If any of the required parameters is empty or None.
        - APIException: If the request fails for any other reason.
        """
        if not recovery_point_id:
            raise InvalidInputException(f"Expected a valid recovery point id, received: `{recovery_point_id}`")
        if not body:
            raise InvalidInputException("Body cannot be empty")
        return self.patch_request(f"/recovery-points/{recovery_point_id}", body=body)

    def post_recovery_point_replicas(self, replicas):
        return self.post_request("/recovery-points/replicas", body=replicas)

    def post_vm_replicas(self, replicas):
        return self.post_request("/vms/replicas", body=replicas)

    def delete_vm_protection_policy(self, vm_syn_id, policy_id):
        return self.delete_request(f"/vms/{vm_syn_id}/policy/{policy_id}")
