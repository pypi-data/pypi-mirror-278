# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetProjectResult',
    'AwaitableGetProjectResult',
    'get_project',
    'get_project_output',
]

@pulumi.output_type
class GetProjectResult:
    """
    A collection of values returned by getProject.
    """
    def __init__(__self__, connection_id=None, docs_job_id=None, freshness_job_id=None, id=None, name=None, project_id=None, repository_id=None, state=None):
        if connection_id and not isinstance(connection_id, int):
            raise TypeError("Expected argument 'connection_id' to be a int")
        pulumi.set(__self__, "connection_id", connection_id)
        if docs_job_id and not isinstance(docs_job_id, int):
            raise TypeError("Expected argument 'docs_job_id' to be a int")
        pulumi.set(__self__, "docs_job_id", docs_job_id)
        if freshness_job_id and not isinstance(freshness_job_id, int):
            raise TypeError("Expected argument 'freshness_job_id' to be a int")
        pulumi.set(__self__, "freshness_job_id", freshness_job_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project_id and not isinstance(project_id, int):
            raise TypeError("Expected argument 'project_id' to be a int")
        pulumi.set(__self__, "project_id", project_id)
        if repository_id and not isinstance(repository_id, int):
            raise TypeError("Expected argument 'repository_id' to be a int")
        pulumi.set(__self__, "repository_id", repository_id)
        if state and not isinstance(state, int):
            raise TypeError("Expected argument 'state' to be a int")
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> int:
        """
        ID of the connection associated with the project
        """
        return pulumi.get(self, "connection_id")

    @property
    @pulumi.getter(name="docsJobId")
    def docs_job_id(self) -> int:
        """
        ID of Job for the documentation
        """
        return pulumi.get(self, "docs_job_id")

    @property
    @pulumi.getter(name="freshnessJobId")
    def freshness_job_id(self) -> int:
        """
        ID of Job for source freshness
        """
        return pulumi.get(self, "freshness_job_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Given name for project
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[int]:
        """
        ID of the project to represent
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="repositoryId")
    def repository_id(self) -> int:
        """
        ID of the repository associated with the project
        """
        return pulumi.get(self, "repository_id")

    @property
    @pulumi.getter
    def state(self) -> int:
        """
        Project state should be 1 = active, as 2 = deleted
        """
        return pulumi.get(self, "state")


class AwaitableGetProjectResult(GetProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectResult(
            connection_id=self.connection_id,
            docs_job_id=self.docs_job_id,
            freshness_job_id=self.freshness_job_id,
            id=self.id,
            name=self.name,
            project_id=self.project_id,
            repository_id=self.repository_id,
            state=self.state)


def get_project(name: Optional[str] = None,
                project_id: Optional[int] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_dbtcloud as dbtcloud

    # projects data sources can use the project_id parameter (preferred uniqueness is ensured)
    test_project = dbtcloud.get_project(project_id=dbt_cloud_project_id)
    # or they can use project names
    # the provider will raise an error if more than one project is found with the same name
    another_test_project = dbtcloud.get_project(name="My other project name")
    ```


    :param str name: Given name for project
    :param int project_id: ID of the project to represent
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('dbtcloud:index/getProject:getProject', __args__, opts=opts, typ=GetProjectResult).value

    return AwaitableGetProjectResult(
        connection_id=pulumi.get(__ret__, 'connection_id'),
        docs_job_id=pulumi.get(__ret__, 'docs_job_id'),
        freshness_job_id=pulumi.get(__ret__, 'freshness_job_id'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        project_id=pulumi.get(__ret__, 'project_id'),
        repository_id=pulumi.get(__ret__, 'repository_id'),
        state=pulumi.get(__ret__, 'state'))


@_utilities.lift_output_func(get_project)
def get_project_output(name: Optional[pulumi.Input[Optional[str]]] = None,
                       project_id: Optional[pulumi.Input[Optional[int]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProjectResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_dbtcloud as dbtcloud

    # projects data sources can use the project_id parameter (preferred uniqueness is ensured)
    test_project = dbtcloud.get_project(project_id=dbt_cloud_project_id)
    # or they can use project names
    # the provider will raise an error if more than one project is found with the same name
    another_test_project = dbtcloud.get_project(name="My other project name")
    ```


    :param str name: Given name for project
    :param int project_id: ID of the project to represent
    """
    ...
