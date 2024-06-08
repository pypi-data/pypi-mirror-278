# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AgentAgentKnowledgeBaseAssociationArgs', 'AgentAgentKnowledgeBaseAssociation']

@pulumi.input_type
class AgentAgentKnowledgeBaseAssociationArgs:
    def __init__(__self__, *,
                 agent_id: pulumi.Input[str],
                 description: pulumi.Input[str],
                 knowledge_base_id: pulumi.Input[str],
                 knowledge_base_state: pulumi.Input[str],
                 agent_version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AgentAgentKnowledgeBaseAssociation resource.
        :param pulumi.Input[str] agent_id: Unique identifier of the agent with which you want to associate the knowledge base.
        :param pulumi.Input[str] description: Description of what the agent should use the knowledge base for.
        :param pulumi.Input[str] knowledge_base_id: Unique identifier of the knowledge base to associate with the agent.
        :param pulumi.Input[str] knowledge_base_state: Whether to use the knowledge base when sending an [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request. Valid values: `ENABLED`, `DISABLED`.
               
               The following arguments are optional:
        :param pulumi.Input[str] agent_version: Version of the agent with which you want to associate the knowledge base. Valid values: `DRAFT`.
        """
        pulumi.set(__self__, "agent_id", agent_id)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "knowledge_base_id", knowledge_base_id)
        pulumi.set(__self__, "knowledge_base_state", knowledge_base_state)
        if agent_version is not None:
            pulumi.set(__self__, "agent_version", agent_version)

    @property
    @pulumi.getter(name="agentId")
    def agent_id(self) -> pulumi.Input[str]:
        """
        Unique identifier of the agent with which you want to associate the knowledge base.
        """
        return pulumi.get(self, "agent_id")

    @agent_id.setter
    def agent_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "agent_id", value)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Input[str]:
        """
        Description of what the agent should use the knowledge base for.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: pulumi.Input[str]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="knowledgeBaseId")
    def knowledge_base_id(self) -> pulumi.Input[str]:
        """
        Unique identifier of the knowledge base to associate with the agent.
        """
        return pulumi.get(self, "knowledge_base_id")

    @knowledge_base_id.setter
    def knowledge_base_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "knowledge_base_id", value)

    @property
    @pulumi.getter(name="knowledgeBaseState")
    def knowledge_base_state(self) -> pulumi.Input[str]:
        """
        Whether to use the knowledge base when sending an [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request. Valid values: `ENABLED`, `DISABLED`.

        The following arguments are optional:
        """
        return pulumi.get(self, "knowledge_base_state")

    @knowledge_base_state.setter
    def knowledge_base_state(self, value: pulumi.Input[str]):
        pulumi.set(self, "knowledge_base_state", value)

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of the agent with which you want to associate the knowledge base. Valid values: `DRAFT`.
        """
        return pulumi.get(self, "agent_version")

    @agent_version.setter
    def agent_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_version", value)


@pulumi.input_type
class _AgentAgentKnowledgeBaseAssociationState:
    def __init__(__self__, *,
                 agent_id: Optional[pulumi.Input[str]] = None,
                 agent_version: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 knowledge_base_id: Optional[pulumi.Input[str]] = None,
                 knowledge_base_state: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AgentAgentKnowledgeBaseAssociation resources.
        :param pulumi.Input[str] agent_id: Unique identifier of the agent with which you want to associate the knowledge base.
        :param pulumi.Input[str] agent_version: Version of the agent with which you want to associate the knowledge base. Valid values: `DRAFT`.
        :param pulumi.Input[str] description: Description of what the agent should use the knowledge base for.
        :param pulumi.Input[str] knowledge_base_id: Unique identifier of the knowledge base to associate with the agent.
        :param pulumi.Input[str] knowledge_base_state: Whether to use the knowledge base when sending an [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request. Valid values: `ENABLED`, `DISABLED`.
               
               The following arguments are optional:
        """
        if agent_id is not None:
            pulumi.set(__self__, "agent_id", agent_id)
        if agent_version is not None:
            pulumi.set(__self__, "agent_version", agent_version)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if knowledge_base_id is not None:
            pulumi.set(__self__, "knowledge_base_id", knowledge_base_id)
        if knowledge_base_state is not None:
            pulumi.set(__self__, "knowledge_base_state", knowledge_base_state)

    @property
    @pulumi.getter(name="agentId")
    def agent_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the agent with which you want to associate the knowledge base.
        """
        return pulumi.get(self, "agent_id")

    @agent_id.setter
    def agent_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_id", value)

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of the agent with which you want to associate the knowledge base. Valid values: `DRAFT`.
        """
        return pulumi.get(self, "agent_version")

    @agent_version.setter
    def agent_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_version", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of what the agent should use the knowledge base for.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="knowledgeBaseId")
    def knowledge_base_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the knowledge base to associate with the agent.
        """
        return pulumi.get(self, "knowledge_base_id")

    @knowledge_base_id.setter
    def knowledge_base_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "knowledge_base_id", value)

    @property
    @pulumi.getter(name="knowledgeBaseState")
    def knowledge_base_state(self) -> Optional[pulumi.Input[str]]:
        """
        Whether to use the knowledge base when sending an [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request. Valid values: `ENABLED`, `DISABLED`.

        The following arguments are optional:
        """
        return pulumi.get(self, "knowledge_base_state")

    @knowledge_base_state.setter
    def knowledge_base_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "knowledge_base_state", value)


class AgentAgentKnowledgeBaseAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_id: Optional[pulumi.Input[str]] = None,
                 agent_version: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 knowledge_base_id: Optional[pulumi.Input[str]] = None,
                 knowledge_base_state: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS Agents for Amazon Bedrock Agent Knowledge Base Association.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.bedrock.AgentAgentKnowledgeBaseAssociation("example",
            agent_id="GGRRAED6JP",
            description="Example Knowledge base",
            knowledge_base_id="EMDPPAYPZI",
            knowledge_base_state="ENABLED")
        ```

        ## Import

        Using `pulumi import`, import Agents for Amazon Bedrock Agent Knowledge Base Association using the agent ID, the agent version, and the knowledge base ID separated by `,`. For example:

        ```sh
        $ pulumi import aws:bedrock/agentAgentKnowledgeBaseAssociation:AgentAgentKnowledgeBaseAssociation example GGRRAED6JP,DRAFT,EMDPPAYPZI
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] agent_id: Unique identifier of the agent with which you want to associate the knowledge base.
        :param pulumi.Input[str] agent_version: Version of the agent with which you want to associate the knowledge base. Valid values: `DRAFT`.
        :param pulumi.Input[str] description: Description of what the agent should use the knowledge base for.
        :param pulumi.Input[str] knowledge_base_id: Unique identifier of the knowledge base to associate with the agent.
        :param pulumi.Input[str] knowledge_base_state: Whether to use the knowledge base when sending an [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request. Valid values: `ENABLED`, `DISABLED`.
               
               The following arguments are optional:
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AgentAgentKnowledgeBaseAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS Agents for Amazon Bedrock Agent Knowledge Base Association.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.bedrock.AgentAgentKnowledgeBaseAssociation("example",
            agent_id="GGRRAED6JP",
            description="Example Knowledge base",
            knowledge_base_id="EMDPPAYPZI",
            knowledge_base_state="ENABLED")
        ```

        ## Import

        Using `pulumi import`, import Agents for Amazon Bedrock Agent Knowledge Base Association using the agent ID, the agent version, and the knowledge base ID separated by `,`. For example:

        ```sh
        $ pulumi import aws:bedrock/agentAgentKnowledgeBaseAssociation:AgentAgentKnowledgeBaseAssociation example GGRRAED6JP,DRAFT,EMDPPAYPZI
        ```

        :param str resource_name: The name of the resource.
        :param AgentAgentKnowledgeBaseAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AgentAgentKnowledgeBaseAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_id: Optional[pulumi.Input[str]] = None,
                 agent_version: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 knowledge_base_id: Optional[pulumi.Input[str]] = None,
                 knowledge_base_state: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AgentAgentKnowledgeBaseAssociationArgs.__new__(AgentAgentKnowledgeBaseAssociationArgs)

            if agent_id is None and not opts.urn:
                raise TypeError("Missing required property 'agent_id'")
            __props__.__dict__["agent_id"] = agent_id
            __props__.__dict__["agent_version"] = agent_version
            if description is None and not opts.urn:
                raise TypeError("Missing required property 'description'")
            __props__.__dict__["description"] = description
            if knowledge_base_id is None and not opts.urn:
                raise TypeError("Missing required property 'knowledge_base_id'")
            __props__.__dict__["knowledge_base_id"] = knowledge_base_id
            if knowledge_base_state is None and not opts.urn:
                raise TypeError("Missing required property 'knowledge_base_state'")
            __props__.__dict__["knowledge_base_state"] = knowledge_base_state
        super(AgentAgentKnowledgeBaseAssociation, __self__).__init__(
            'aws:bedrock/agentAgentKnowledgeBaseAssociation:AgentAgentKnowledgeBaseAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            agent_id: Optional[pulumi.Input[str]] = None,
            agent_version: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            knowledge_base_id: Optional[pulumi.Input[str]] = None,
            knowledge_base_state: Optional[pulumi.Input[str]] = None) -> 'AgentAgentKnowledgeBaseAssociation':
        """
        Get an existing AgentAgentKnowledgeBaseAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] agent_id: Unique identifier of the agent with which you want to associate the knowledge base.
        :param pulumi.Input[str] agent_version: Version of the agent with which you want to associate the knowledge base. Valid values: `DRAFT`.
        :param pulumi.Input[str] description: Description of what the agent should use the knowledge base for.
        :param pulumi.Input[str] knowledge_base_id: Unique identifier of the knowledge base to associate with the agent.
        :param pulumi.Input[str] knowledge_base_state: Whether to use the knowledge base when sending an [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request. Valid values: `ENABLED`, `DISABLED`.
               
               The following arguments are optional:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AgentAgentKnowledgeBaseAssociationState.__new__(_AgentAgentKnowledgeBaseAssociationState)

        __props__.__dict__["agent_id"] = agent_id
        __props__.__dict__["agent_version"] = agent_version
        __props__.__dict__["description"] = description
        __props__.__dict__["knowledge_base_id"] = knowledge_base_id
        __props__.__dict__["knowledge_base_state"] = knowledge_base_state
        return AgentAgentKnowledgeBaseAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentId")
    def agent_id(self) -> pulumi.Output[str]:
        """
        Unique identifier of the agent with which you want to associate the knowledge base.
        """
        return pulumi.get(self, "agent_id")

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> pulumi.Output[str]:
        """
        Version of the agent with which you want to associate the knowledge base. Valid values: `DRAFT`.
        """
        return pulumi.get(self, "agent_version")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Description of what the agent should use the knowledge base for.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="knowledgeBaseId")
    def knowledge_base_id(self) -> pulumi.Output[str]:
        """
        Unique identifier of the knowledge base to associate with the agent.
        """
        return pulumi.get(self, "knowledge_base_id")

    @property
    @pulumi.getter(name="knowledgeBaseState")
    def knowledge_base_state(self) -> pulumi.Output[str]:
        """
        Whether to use the knowledge base when sending an [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request. Valid values: `ENABLED`, `DISABLED`.

        The following arguments are optional:
        """
        return pulumi.get(self, "knowledge_base_state")

