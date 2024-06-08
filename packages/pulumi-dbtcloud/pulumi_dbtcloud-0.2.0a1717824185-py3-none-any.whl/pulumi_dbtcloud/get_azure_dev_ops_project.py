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
    'GetAzureDevOpsProjectResult',
    'AwaitableGetAzureDevOpsProjectResult',
    'get_azure_dev_ops_project',
    'get_azure_dev_ops_project_output',
]

@pulumi.output_type
class GetAzureDevOpsProjectResult:
    """
    A collection of values returned by getAzureDevOpsProject.
    """
    def __init__(__self__, id=None, name=None, url=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The internal Azure Dev Ops ID of the ADO Project
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the ADO project
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        The URL of the ADO project
        """
        return pulumi.get(self, "url")


class AwaitableGetAzureDevOpsProjectResult(GetAzureDevOpsProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAzureDevOpsProjectResult(
            id=self.id,
            name=self.name,
            url=self.url)


def get_azure_dev_ops_project(name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAzureDevOpsProjectResult:
    """
    Use this data source to retrieve the ID of an Azure Dev Ops project
    based on its name.

    This data source requires connecting with a user token and doesn't work with a service token.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_dbtcloud as dbtcloud

    my_ado_project = dbtcloud.get_azure_dev_ops_project(name="my-project-name")
    ```


    :param str name: The name of the ADO project
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('dbtcloud:index/getAzureDevOpsProject:getAzureDevOpsProject', __args__, opts=opts, typ=GetAzureDevOpsProjectResult).value

    return AwaitableGetAzureDevOpsProjectResult(
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        url=pulumi.get(__ret__, 'url'))


@_utilities.lift_output_func(get_azure_dev_ops_project)
def get_azure_dev_ops_project_output(name: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAzureDevOpsProjectResult]:
    """
    Use this data source to retrieve the ID of an Azure Dev Ops project
    based on its name.

    This data source requires connecting with a user token and doesn't work with a service token.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_dbtcloud as dbtcloud

    my_ado_project = dbtcloud.get_azure_dev_ops_project(name="my-project-name")
    ```


    :param str name: The name of the ADO project
    """
    ...
