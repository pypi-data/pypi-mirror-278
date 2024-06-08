# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ProjectConnectionArgs', 'ProjectConnection']

@pulumi.input_type
class ProjectConnectionArgs:
    def __init__(__self__, *,
                 connection_id: pulumi.Input[int],
                 project_id: pulumi.Input[int]):
        """
        The set of arguments for constructing a ProjectConnection resource.
        :param pulumi.Input[int] connection_id: Connection ID
        :param pulumi.Input[int] project_id: Project ID
        """
        pulumi.set(__self__, "connection_id", connection_id)
        pulumi.set(__self__, "project_id", project_id)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> pulumi.Input[int]:
        """
        Connection ID
        """
        return pulumi.get(self, "connection_id")

    @connection_id.setter
    def connection_id(self, value: pulumi.Input[int]):
        pulumi.set(self, "connection_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Input[int]:
        """
        Project ID
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: pulumi.Input[int]):
        pulumi.set(self, "project_id", value)


@pulumi.input_type
class _ProjectConnectionState:
    def __init__(__self__, *,
                 connection_id: Optional[pulumi.Input[int]] = None,
                 project_id: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering ProjectConnection resources.
        :param pulumi.Input[int] connection_id: Connection ID
        :param pulumi.Input[int] project_id: Project ID
        """
        if connection_id is not None:
            pulumi.set(__self__, "connection_id", connection_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> Optional[pulumi.Input[int]]:
        """
        Connection ID
        """
        return pulumi.get(self, "connection_id")

    @connection_id.setter
    def connection_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "connection_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[int]]:
        """
        Project ID
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "project_id", value)


class ProjectConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_id: Optional[pulumi.Input[int]] = None,
                 project_id: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_dbtcloud as dbtcloud

        dbt_project_connection = dbtcloud.ProjectConnection("dbt_project_connection",
            project_id=dbt_project["id"],
            connection_id=dbt_connection["connectionId"])
        ```

        ## Import

        using  import blocks (requires Terraform >= 1.5)

        import {

          to = dbtcloud_project_connection.my_project

          id = "project_id:connection_id"

        }

        import {

          to = dbtcloud_project_connection.my_project

          id = "12345:5678"

        }

        using the older import command

        ```sh
        $ pulumi import dbtcloud:index/projectConnection:ProjectConnection my_project "project_id:connection_id"
        ```

        ```sh
        $ pulumi import dbtcloud:index/projectConnection:ProjectConnection my_project 12345:5678
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] connection_id: Connection ID
        :param pulumi.Input[int] project_id: Project ID
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProjectConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_dbtcloud as dbtcloud

        dbt_project_connection = dbtcloud.ProjectConnection("dbt_project_connection",
            project_id=dbt_project["id"],
            connection_id=dbt_connection["connectionId"])
        ```

        ## Import

        using  import blocks (requires Terraform >= 1.5)

        import {

          to = dbtcloud_project_connection.my_project

          id = "project_id:connection_id"

        }

        import {

          to = dbtcloud_project_connection.my_project

          id = "12345:5678"

        }

        using the older import command

        ```sh
        $ pulumi import dbtcloud:index/projectConnection:ProjectConnection my_project "project_id:connection_id"
        ```

        ```sh
        $ pulumi import dbtcloud:index/projectConnection:ProjectConnection my_project 12345:5678
        ```

        :param str resource_name: The name of the resource.
        :param ProjectConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProjectConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_id: Optional[pulumi.Input[int]] = None,
                 project_id: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProjectConnectionArgs.__new__(ProjectConnectionArgs)

            if connection_id is None and not opts.urn:
                raise TypeError("Missing required property 'connection_id'")
            __props__.__dict__["connection_id"] = connection_id
            if project_id is None and not opts.urn:
                raise TypeError("Missing required property 'project_id'")
            __props__.__dict__["project_id"] = project_id
        super(ProjectConnection, __self__).__init__(
            'dbtcloud:index/projectConnection:ProjectConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            connection_id: Optional[pulumi.Input[int]] = None,
            project_id: Optional[pulumi.Input[int]] = None) -> 'ProjectConnection':
        """
        Get an existing ProjectConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] connection_id: Connection ID
        :param pulumi.Input[int] project_id: Project ID
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ProjectConnectionState.__new__(_ProjectConnectionState)

        __props__.__dict__["connection_id"] = connection_id
        __props__.__dict__["project_id"] = project_id
        return ProjectConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> pulumi.Output[int]:
        """
        Connection ID
        """
        return pulumi.get(self, "connection_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[int]:
        """
        Project ID
        """
        return pulumi.get(self, "project_id")

