# coding=utf-8
# *** WARNING: this file was generated by pulumi-gen-eks. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
import pulumi_aws

__all__ = ['NodeGroupSecurityGroupArgs', 'NodeGroupSecurityGroup']

@pulumi.input_type
class NodeGroupSecurityGroupArgs:
    def __init__(__self__, *,
                 cluster_security_group: pulumi.Input['pulumi_aws.ec2.SecurityGroup'],
                 eks_cluster: pulumi.Input['pulumi_aws.eks.Cluster'],
                 vpc_id: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NodeGroupSecurityGroup resource.
        :param pulumi.Input['pulumi_aws.ec2.SecurityGroup'] cluster_security_group: The security group associated with the EKS cluster.
        :param pulumi.Input['pulumi_aws.eks.Cluster'] eks_cluster: The EKS cluster associated with the worker node group
        :param pulumi.Input[str] vpc_id: The VPC in which to create the worker node group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of tags to apply to this security group.
        """
        pulumi.set(__self__, "cluster_security_group", cluster_security_group)
        pulumi.set(__self__, "eks_cluster", eks_cluster)
        pulumi.set(__self__, "vpc_id", vpc_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="clusterSecurityGroup")
    def cluster_security_group(self) -> pulumi.Input['pulumi_aws.ec2.SecurityGroup']:
        """
        The security group associated with the EKS cluster.
        """
        return pulumi.get(self, "cluster_security_group")

    @cluster_security_group.setter
    def cluster_security_group(self, value: pulumi.Input['pulumi_aws.ec2.SecurityGroup']):
        pulumi.set(self, "cluster_security_group", value)

    @property
    @pulumi.getter(name="eksCluster")
    def eks_cluster(self) -> pulumi.Input['pulumi_aws.eks.Cluster']:
        """
        The EKS cluster associated with the worker node group
        """
        return pulumi.get(self, "eks_cluster")

    @eks_cluster.setter
    def eks_cluster(self, value: pulumi.Input['pulumi_aws.eks.Cluster']):
        pulumi.set(self, "eks_cluster", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The VPC in which to create the worker node group.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value mapping of tags to apply to this security group.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class NodeGroupSecurityGroup(pulumi.ComponentResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_security_group: Optional[pulumi.Input['pulumi_aws.ec2.SecurityGroup']] = None,
                 eks_cluster: Optional[pulumi.Input['pulumi_aws.eks.Cluster']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        NodeGroupSecurityGroup is a component that wraps creating a security group for node groups with the default ingress & egress rules required to connect and work with the EKS cluster security group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input['pulumi_aws.ec2.SecurityGroup'] cluster_security_group: The security group associated with the EKS cluster.
        :param pulumi.Input['pulumi_aws.eks.Cluster'] eks_cluster: The EKS cluster associated with the worker node group
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of tags to apply to this security group.
        :param pulumi.Input[str] vpc_id: The VPC in which to create the worker node group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NodeGroupSecurityGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        NodeGroupSecurityGroup is a component that wraps creating a security group for node groups with the default ingress & egress rules required to connect and work with the EKS cluster security group.

        :param str resource_name: The name of the resource.
        :param NodeGroupSecurityGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NodeGroupSecurityGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_security_group: Optional[pulumi.Input['pulumi_aws.ec2.SecurityGroup']] = None,
                 eks_cluster: Optional[pulumi.Input['pulumi_aws.eks.Cluster']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is not None:
            raise ValueError('ComponentResource classes do not support opts.id')
        else:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NodeGroupSecurityGroupArgs.__new__(NodeGroupSecurityGroupArgs)

            if cluster_security_group is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_security_group'")
            __props__.__dict__["cluster_security_group"] = cluster_security_group
            if eks_cluster is None and not opts.urn:
                raise TypeError("Missing required property 'eks_cluster'")
            __props__.__dict__["eks_cluster"] = eks_cluster
            __props__.__dict__["tags"] = tags
            if vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__["vpc_id"] = vpc_id
            __props__.__dict__["security_group"] = None
            __props__.__dict__["security_group_rule"] = None
        super(NodeGroupSecurityGroup, __self__).__init__(
            'eks:index:NodeGroupSecurityGroup',
            resource_name,
            __props__,
            opts,
            remote=True)

    @property
    @pulumi.getter(name="securityGroup")
    def security_group(self) -> pulumi.Output['pulumi_aws.ec2.SecurityGroup']:
        """
        The security group for node groups with the default ingress & egress rules required to connect and work with the EKS cluster security group.
        """
        return pulumi.get(self, "security_group")

    @property
    @pulumi.getter(name="securityGroupRule")
    def security_group_rule(self) -> pulumi.Output['pulumi_aws.ec2.SecurityGroupRule']:
        """
        The EKS cluster ingress rule.
        """
        return pulumi.get(self, "security_group_rule")

