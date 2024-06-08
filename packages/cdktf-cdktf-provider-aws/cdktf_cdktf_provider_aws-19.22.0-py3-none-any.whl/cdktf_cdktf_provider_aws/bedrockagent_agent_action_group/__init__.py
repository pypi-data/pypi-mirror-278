'''
# `aws_bedrockagent_agent_action_group`

Refer to the Terraform Registry for docs: [`aws_bedrockagent_agent_action_group`](https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class BedrockagentAgentActionGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group aws_bedrockagent_agent_action_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        action_group_name: builtins.str,
        agent_id: builtins.str,
        agent_version: builtins.str,
        action_group_executor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentAgentActionGroupActionGroupExecutor", typing.Dict[builtins.str, typing.Any]]]]] = None,
        action_group_state: typing.Optional[builtins.str] = None,
        api_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentAgentActionGroupApiSchema", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        parent_action_group_signature: typing.Optional[builtins.str] = None,
        skip_resource_in_use_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group aws_bedrockagent_agent_action_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#action_group_name BedrockagentAgentActionGroup#action_group_name}.
        :param agent_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#agent_id BedrockagentAgentActionGroup#agent_id}.
        :param agent_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#agent_version BedrockagentAgentActionGroup#agent_version}.
        :param action_group_executor: action_group_executor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#action_group_executor BedrockagentAgentActionGroup#action_group_executor}
        :param action_group_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#action_group_state BedrockagentAgentActionGroup#action_group_state}.
        :param api_schema: api_schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#api_schema BedrockagentAgentActionGroup#api_schema}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#description BedrockagentAgentActionGroup#description}.
        :param parent_action_group_signature: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#parent_action_group_signature BedrockagentAgentActionGroup#parent_action_group_signature}.
        :param skip_resource_in_use_check: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#skip_resource_in_use_check BedrockagentAgentActionGroup#skip_resource_in_use_check}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9363e2908e49434c59839cce14680f56d528608e8b3e7f27d1bf59d6e52055e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = BedrockagentAgentActionGroupConfig(
            action_group_name=action_group_name,
            agent_id=agent_id,
            agent_version=agent_version,
            action_group_executor=action_group_executor,
            action_group_state=action_group_state,
            api_schema=api_schema,
            description=description,
            parent_action_group_signature=parent_action_group_signature,
            skip_resource_in_use_check=skip_resource_in_use_check,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a BedrockagentAgentActionGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BedrockagentAgentActionGroup to import.
        :param import_from_id: The id of the existing BedrockagentAgentActionGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BedrockagentAgentActionGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc7cf0e008eeed2214bc28485ac5772485cedb3b0752459792ce9763dd4698a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActionGroupExecutor")
    def put_action_group_executor(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentAgentActionGroupActionGroupExecutor", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c43040811bdde5e2047cebf6808885faf1d02f5d82ff61defdee38cd13f569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActionGroupExecutor", [value]))

    @jsii.member(jsii_name="putApiSchema")
    def put_api_schema(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentAgentActionGroupApiSchema", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69f83fa406e4b115f32ce64ad24eb5d69ff82b5ae50febd4e61308e63ca54dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApiSchema", [value]))

    @jsii.member(jsii_name="resetActionGroupExecutor")
    def reset_action_group_executor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionGroupExecutor", []))

    @jsii.member(jsii_name="resetActionGroupState")
    def reset_action_group_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionGroupState", []))

    @jsii.member(jsii_name="resetApiSchema")
    def reset_api_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiSchema", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetParentActionGroupSignature")
    def reset_parent_action_group_signature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentActionGroupSignature", []))

    @jsii.member(jsii_name="resetSkipResourceInUseCheck")
    def reset_skip_resource_in_use_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipResourceInUseCheck", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupExecutor")
    def action_group_executor(
        self,
    ) -> "BedrockagentAgentActionGroupActionGroupExecutorList":
        return typing.cast("BedrockagentAgentActionGroupActionGroupExecutorList", jsii.get(self, "actionGroupExecutor"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupId")
    def action_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionGroupId"))

    @builtins.property
    @jsii.member(jsii_name="apiSchema")
    def api_schema(self) -> "BedrockagentAgentActionGroupApiSchemaList":
        return typing.cast("BedrockagentAgentActionGroupApiSchemaList", jsii.get(self, "apiSchema"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupExecutorInput")
    def action_group_executor_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentAgentActionGroupActionGroupExecutor"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentAgentActionGroupActionGroupExecutor"]]], jsii.get(self, "actionGroupExecutorInput"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupNameInput")
    def action_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupStateInput")
    def action_group_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionGroupStateInput"))

    @builtins.property
    @jsii.member(jsii_name="agentIdInput")
    def agent_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="agentVersionInput")
    def agent_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSchemaInput")
    def api_schema_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentAgentActionGroupApiSchema"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentAgentActionGroupApiSchema"]]], jsii.get(self, "apiSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="parentActionGroupSignatureInput")
    def parent_action_group_signature_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentActionGroupSignatureInput"))

    @builtins.property
    @jsii.member(jsii_name="skipResourceInUseCheckInput")
    def skip_resource_in_use_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipResourceInUseCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupName")
    def action_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionGroupName"))

    @action_group_name.setter
    def action_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1375953ad8105174ba2e1b88af6fd5a3814585a8738959b92e8d4b5f22730b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="actionGroupState")
    def action_group_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionGroupState"))

    @action_group_state.setter
    def action_group_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ef8065e9734c6a7826d10df92326c37d15501d386c0477485d98b7c2365a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionGroupState", value)

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @agent_id.setter
    def agent_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1264bbf035a55a4cfe0f89645dc0e18306dd9a4c094d57d944e1b721fee4f7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentId", value)

    @builtins.property
    @jsii.member(jsii_name="agentVersion")
    def agent_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentVersion"))

    @agent_version.setter
    def agent_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af298cd4ea3ff851483aec698f7e1904b4c8b70a1bc2ed3518a9446adb9d0944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentVersion", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320e325ea05d3ca00fd154b32d7b6cc7329fe30a88d9471a87bc442f54285e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="parentActionGroupSignature")
    def parent_action_group_signature(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentActionGroupSignature"))

    @parent_action_group_signature.setter
    def parent_action_group_signature(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86567d8fb1e8f54496a24a4e064211e03495c73aa95869a73f3d8126591c3e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentActionGroupSignature", value)

    @builtins.property
    @jsii.member(jsii_name="skipResourceInUseCheck")
    def skip_resource_in_use_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipResourceInUseCheck"))

    @skip_resource_in_use_check.setter
    def skip_resource_in_use_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8f03df3d35571ff828e1c137c0e5fda627ad5c6424a88151bc9dc810491a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipResourceInUseCheck", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroupActionGroupExecutor",
    jsii_struct_bases=[],
    name_mapping={"lambda_": "lambda"},
)
class BedrockagentAgentActionGroupActionGroupExecutor:
    def __init__(self, *, lambda_: typing.Optional[builtins.str] = None) -> None:
        '''
        :param lambda_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#lambda BedrockagentAgentActionGroup#lambda}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16f8e683435c1a184a9190bf17c5aed733af9d87c14c96ee49c6450e6583255)
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lambda_ is not None:
            self._values["lambda_"] = lambda_

    @builtins.property
    def lambda_(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#lambda BedrockagentAgentActionGroup#lambda}.'''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentAgentActionGroupActionGroupExecutor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentAgentActionGroupActionGroupExecutorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroupActionGroupExecutorList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f20a3391632a36a2e7f3d24b24950cb41b3a010d631b474543eae76d3de3de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentAgentActionGroupActionGroupExecutorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ee760aad8aa0edc0cb835cfdb5c3fc661907848e07d5f2247552d4ed3f6b3a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentAgentActionGroupActionGroupExecutorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f01af4b6df7da9faef62fad2c76d0085dafda444a466f32c8f7bbfd31d20141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8802b14cb82a2d792672ffca55b8222f86d534b22ee6a02eb81c9cd315fee20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0337e7ed29886b9bf9bf92d1890bc3e45d7a0bd00a82f276491fac04ec8cccd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupActionGroupExecutor]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupActionGroupExecutor]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupActionGroupExecutor]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b7f8f971dd554a416e8af6d7701536ffb723538036972694126bef4a9b0941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BedrockagentAgentActionGroupActionGroupExecutorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroupActionGroupExecutorOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1400ee992354b41c20a48d593aee25698f51e2fc8d0ba631db2adfabf30cf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLambda")
    def reset_lambda(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambda", []))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambda"))

    @lambda_.setter
    def lambda_(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006014213d9c0890b7525376c4735fdf9d8da82ed074c25a89dd5e489ecbac76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambda", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupActionGroupExecutor]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupActionGroupExecutor]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupActionGroupExecutor]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc6525c3c687d0cab9f580e0f2cc92086919f1ec867da61acbf05a6f2f3bcbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroupApiSchema",
    jsii_struct_bases=[],
    name_mapping={"payload": "payload", "s3": "s3"},
)
class BedrockagentAgentActionGroupApiSchema:
    def __init__(
        self,
        *,
        payload: typing.Optional[builtins.str] = None,
        s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentAgentActionGroupApiSchemaS3", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param payload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#payload BedrockagentAgentActionGroup#payload}.
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#s3 BedrockagentAgentActionGroup#s3}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc9e7872ad4e526a6a893677a803e2345c323dc97fc2c519e29fad5cd25033a9)
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if payload is not None:
            self._values["payload"] = payload
        if s3 is not None:
            self._values["s3"] = s3

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#payload BedrockagentAgentActionGroup#payload}.'''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentAgentActionGroupApiSchemaS3"]]]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#s3 BedrockagentAgentActionGroup#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentAgentActionGroupApiSchemaS3"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentAgentActionGroupApiSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentAgentActionGroupApiSchemaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroupApiSchemaList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25452aa09fa22b890d6294737257687bde8f1c0ee9dd1bba1702e67f8fa327d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentAgentActionGroupApiSchemaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3d469a5454137aa8b7369c1ba71022cfd407d5610940d5c0f6cb1446a728c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentAgentActionGroupApiSchemaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d644eb6d008466d60a68652f56c516cd0a682d9b4d1d1e7bfe31be8b0ac87184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a249f78e1feebb8b9669371319e12dde111c6104ea700b070eae895d5e38654a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6c6896df33825ad3817ab65780d1ce365b1cedf93f8633da142e90c3506e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupApiSchema]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupApiSchema]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupApiSchema]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6c35aeb9f31a98c0b502fd6ceaa9d94a6d0e30c1414a8749336e97df8cfd9a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BedrockagentAgentActionGroupApiSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroupApiSchemaOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0086e0709aeac93a1f48c9b103a0c6f6cc22e6d80b46820091da66b69200410)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentAgentActionGroupApiSchemaS3", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338aab08294f4bed7cb4345628670d249be3c244cd09abb5dc0188d189bce7db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="resetPayload")
    def reset_payload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayload", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "BedrockagentAgentActionGroupApiSchemaS3List":
        return typing.cast("BedrockagentAgentActionGroupApiSchemaS3List", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="payloadInput")
    def payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentAgentActionGroupApiSchemaS3"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentAgentActionGroupApiSchemaS3"]]], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba5fd3f7bcdfbd0443e0b93f708ef52d6c7caa36ae9029bc9608b9bec018e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupApiSchema]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupApiSchema]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupApiSchema]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd913abde87e3ee0f65c9f06be67ee3f3f118e18f42f38dada193faddbcac5f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroupApiSchemaS3",
    jsii_struct_bases=[],
    name_mapping={"s3_bucket_name": "s3BucketName", "s3_object_key": "s3ObjectKey"},
)
class BedrockagentAgentActionGroupApiSchemaS3:
    def __init__(
        self,
        *,
        s3_bucket_name: typing.Optional[builtins.str] = None,
        s3_object_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#s3_bucket_name BedrockagentAgentActionGroup#s3_bucket_name}.
        :param s3_object_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#s3_object_key BedrockagentAgentActionGroup#s3_object_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbaf314391f581290f3072a95d25a25e5dd484a5b4f720a44473688c242fc36)
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument s3_object_key", value=s3_object_key, expected_type=type_hints["s3_object_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_bucket_name is not None:
            self._values["s3_bucket_name"] = s3_bucket_name
        if s3_object_key is not None:
            self._values["s3_object_key"] = s3_object_key

    @builtins.property
    def s3_bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#s3_bucket_name BedrockagentAgentActionGroup#s3_bucket_name}.'''
        result = self._values.get("s3_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_object_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#s3_object_key BedrockagentAgentActionGroup#s3_object_key}.'''
        result = self._values.get("s3_object_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentAgentActionGroupApiSchemaS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentAgentActionGroupApiSchemaS3List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroupApiSchemaS3List",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7b7157bd14ae4ee2155385836e57491c3c4f0e79d3f2bedd05af6526432a55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentAgentActionGroupApiSchemaS3OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1e05dc1ccd185a5181c1bf91a25e01f8964bf4079ec30f19a7e9a5f38714a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentAgentActionGroupApiSchemaS3OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc5e96f3ad1c7e09bad00129eeed66177623486b33a6e96431dc75d38cdac08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7904ee991b006ee04c2181d81a3ad07316aeb2ebb812270e84893f705bf8ae0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101e199109dcb2762caaa0ecdb7d32871e4c30ccc1cc472e448264240405d83e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupApiSchemaS3]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupApiSchemaS3]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupApiSchemaS3]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff2a20802da51e398928a30888c250ecbda3562d6d1adf8f739b2cf9ad3daf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BedrockagentAgentActionGroupApiSchemaS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroupApiSchemaS3OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a30fd4afba5776ee854fc1d3024dee4eb5b4852e1bbbb6f253c26ffaee4d71b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetS3BucketName")
    def reset_s3_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BucketName", []))

    @jsii.member(jsii_name="resetS3ObjectKey")
    def reset_s3_object_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3ObjectKey", []))

    @builtins.property
    @jsii.member(jsii_name="s3BucketNameInput")
    def s3_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3ObjectKeyInput")
    def s3_object_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3ObjectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketName"))

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77b59cad1035cb08209101cc46145c0e068040ea4d47b047d3f334b2f1de69b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketName", value)

    @builtins.property
    @jsii.member(jsii_name="s3ObjectKey")
    def s3_object_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3ObjectKey"))

    @s3_object_key.setter
    def s3_object_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967582586ab9a24e03654fc59c9eecef3de92d3957e0db1aab9c39c448abb002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3ObjectKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupApiSchemaS3]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupApiSchemaS3]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupApiSchemaS3]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d69a58b1d705db3edaa1d39ed4fb502898fd964b81cbc749d22b82e0a17826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentAgentActionGroup.BedrockagentAgentActionGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action_group_name": "actionGroupName",
        "agent_id": "agentId",
        "agent_version": "agentVersion",
        "action_group_executor": "actionGroupExecutor",
        "action_group_state": "actionGroupState",
        "api_schema": "apiSchema",
        "description": "description",
        "parent_action_group_signature": "parentActionGroupSignature",
        "skip_resource_in_use_check": "skipResourceInUseCheck",
    },
)
class BedrockagentAgentActionGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        action_group_name: builtins.str,
        agent_id: builtins.str,
        agent_version: builtins.str,
        action_group_executor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentAgentActionGroupActionGroupExecutor, typing.Dict[builtins.str, typing.Any]]]]] = None,
        action_group_state: typing.Optional[builtins.str] = None,
        api_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentAgentActionGroupApiSchema, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        parent_action_group_signature: typing.Optional[builtins.str] = None,
        skip_resource_in_use_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#action_group_name BedrockagentAgentActionGroup#action_group_name}.
        :param agent_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#agent_id BedrockagentAgentActionGroup#agent_id}.
        :param agent_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#agent_version BedrockagentAgentActionGroup#agent_version}.
        :param action_group_executor: action_group_executor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#action_group_executor BedrockagentAgentActionGroup#action_group_executor}
        :param action_group_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#action_group_state BedrockagentAgentActionGroup#action_group_state}.
        :param api_schema: api_schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#api_schema BedrockagentAgentActionGroup#api_schema}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#description BedrockagentAgentActionGroup#description}.
        :param parent_action_group_signature: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#parent_action_group_signature BedrockagentAgentActionGroup#parent_action_group_signature}.
        :param skip_resource_in_use_check: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#skip_resource_in_use_check BedrockagentAgentActionGroup#skip_resource_in_use_check}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a69bdaab037a4b0d06eaa2ecef933beb455ebca382db9b3ce756e3ad65fca7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action_group_name", value=action_group_name, expected_type=type_hints["action_group_name"])
            check_type(argname="argument agent_id", value=agent_id, expected_type=type_hints["agent_id"])
            check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            check_type(argname="argument action_group_executor", value=action_group_executor, expected_type=type_hints["action_group_executor"])
            check_type(argname="argument action_group_state", value=action_group_state, expected_type=type_hints["action_group_state"])
            check_type(argname="argument api_schema", value=api_schema, expected_type=type_hints["api_schema"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parent_action_group_signature", value=parent_action_group_signature, expected_type=type_hints["parent_action_group_signature"])
            check_type(argname="argument skip_resource_in_use_check", value=skip_resource_in_use_check, expected_type=type_hints["skip_resource_in_use_check"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_group_name": action_group_name,
            "agent_id": agent_id,
            "agent_version": agent_version,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if action_group_executor is not None:
            self._values["action_group_executor"] = action_group_executor
        if action_group_state is not None:
            self._values["action_group_state"] = action_group_state
        if api_schema is not None:
            self._values["api_schema"] = api_schema
        if description is not None:
            self._values["description"] = description
        if parent_action_group_signature is not None:
            self._values["parent_action_group_signature"] = parent_action_group_signature
        if skip_resource_in_use_check is not None:
            self._values["skip_resource_in_use_check"] = skip_resource_in_use_check

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def action_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#action_group_name BedrockagentAgentActionGroup#action_group_name}.'''
        result = self._values.get("action_group_name")
        assert result is not None, "Required property 'action_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#agent_id BedrockagentAgentActionGroup#agent_id}.'''
        result = self._values.get("agent_id")
        assert result is not None, "Required property 'agent_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#agent_version BedrockagentAgentActionGroup#agent_version}.'''
        result = self._values.get("agent_version")
        assert result is not None, "Required property 'agent_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_group_executor(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupActionGroupExecutor]]]:
        '''action_group_executor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#action_group_executor BedrockagentAgentActionGroup#action_group_executor}
        '''
        result = self._values.get("action_group_executor")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupActionGroupExecutor]]], result)

    @builtins.property
    def action_group_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#action_group_state BedrockagentAgentActionGroup#action_group_state}.'''
        result = self._values.get("action_group_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_schema(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupApiSchema]]]:
        '''api_schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#api_schema BedrockagentAgentActionGroup#api_schema}
        '''
        result = self._values.get("api_schema")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupApiSchema]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#description BedrockagentAgentActionGroup#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_action_group_signature(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#parent_action_group_signature BedrockagentAgentActionGroup#parent_action_group_signature}.'''
        result = self._values.get("parent_action_group_signature")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_resource_in_use_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.53.0/docs/resources/bedrockagent_agent_action_group#skip_resource_in_use_check BedrockagentAgentActionGroup#skip_resource_in_use_check}.'''
        result = self._values.get("skip_resource_in_use_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentAgentActionGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BedrockagentAgentActionGroup",
    "BedrockagentAgentActionGroupActionGroupExecutor",
    "BedrockagentAgentActionGroupActionGroupExecutorList",
    "BedrockagentAgentActionGroupActionGroupExecutorOutputReference",
    "BedrockagentAgentActionGroupApiSchema",
    "BedrockagentAgentActionGroupApiSchemaList",
    "BedrockagentAgentActionGroupApiSchemaOutputReference",
    "BedrockagentAgentActionGroupApiSchemaS3",
    "BedrockagentAgentActionGroupApiSchemaS3List",
    "BedrockagentAgentActionGroupApiSchemaS3OutputReference",
    "BedrockagentAgentActionGroupConfig",
]

publication.publish()

def _typecheckingstub__9363e2908e49434c59839cce14680f56d528608e8b3e7f27d1bf59d6e52055e6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    action_group_name: builtins.str,
    agent_id: builtins.str,
    agent_version: builtins.str,
    action_group_executor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentAgentActionGroupActionGroupExecutor, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action_group_state: typing.Optional[builtins.str] = None,
    api_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentAgentActionGroupApiSchema, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    parent_action_group_signature: typing.Optional[builtins.str] = None,
    skip_resource_in_use_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc7cf0e008eeed2214bc28485ac5772485cedb3b0752459792ce9763dd4698a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c43040811bdde5e2047cebf6808885faf1d02f5d82ff61defdee38cd13f569(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentAgentActionGroupActionGroupExecutor, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69f83fa406e4b115f32ce64ad24eb5d69ff82b5ae50febd4e61308e63ca54dd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentAgentActionGroupApiSchema, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1375953ad8105174ba2e1b88af6fd5a3814585a8738959b92e8d4b5f22730b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ef8065e9734c6a7826d10df92326c37d15501d386c0477485d98b7c2365a21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1264bbf035a55a4cfe0f89645dc0e18306dd9a4c094d57d944e1b721fee4f7bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af298cd4ea3ff851483aec698f7e1904b4c8b70a1bc2ed3518a9446adb9d0944(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320e325ea05d3ca00fd154b32d7b6cc7329fe30a88d9471a87bc442f54285e32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86567d8fb1e8f54496a24a4e064211e03495c73aa95869a73f3d8126591c3e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8f03df3d35571ff828e1c137c0e5fda627ad5c6424a88151bc9dc810491a4e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16f8e683435c1a184a9190bf17c5aed733af9d87c14c96ee49c6450e6583255(
    *,
    lambda_: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f20a3391632a36a2e7f3d24b24950cb41b3a010d631b474543eae76d3de3de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ee760aad8aa0edc0cb835cfdb5c3fc661907848e07d5f2247552d4ed3f6b3a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f01af4b6df7da9faef62fad2c76d0085dafda444a466f32c8f7bbfd31d20141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8802b14cb82a2d792672ffca55b8222f86d534b22ee6a02eb81c9cd315fee20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0337e7ed29886b9bf9bf92d1890bc3e45d7a0bd00a82f276491fac04ec8cccd5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b7f8f971dd554a416e8af6d7701536ffb723538036972694126bef4a9b0941(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupActionGroupExecutor]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1400ee992354b41c20a48d593aee25698f51e2fc8d0ba631db2adfabf30cf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006014213d9c0890b7525376c4735fdf9d8da82ed074c25a89dd5e489ecbac76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc6525c3c687d0cab9f580e0f2cc92086919f1ec867da61acbf05a6f2f3bcbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupActionGroupExecutor]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9e7872ad4e526a6a893677a803e2345c323dc97fc2c519e29fad5cd25033a9(
    *,
    payload: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentAgentActionGroupApiSchemaS3, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25452aa09fa22b890d6294737257687bde8f1c0ee9dd1bba1702e67f8fa327d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3d469a5454137aa8b7369c1ba71022cfd407d5610940d5c0f6cb1446a728c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d644eb6d008466d60a68652f56c516cd0a682d9b4d1d1e7bfe31be8b0ac87184(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a249f78e1feebb8b9669371319e12dde111c6104ea700b070eae895d5e38654a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6c6896df33825ad3817ab65780d1ce365b1cedf93f8633da142e90c3506e1d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c35aeb9f31a98c0b502fd6ceaa9d94a6d0e30c1414a8749336e97df8cfd9a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupApiSchema]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0086e0709aeac93a1f48c9b103a0c6f6cc22e6d80b46820091da66b69200410(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338aab08294f4bed7cb4345628670d249be3c244cd09abb5dc0188d189bce7db(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentAgentActionGroupApiSchemaS3, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba5fd3f7bcdfbd0443e0b93f708ef52d6c7caa36ae9029bc9608b9bec018e68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd913abde87e3ee0f65c9f06be67ee3f3f118e18f42f38dada193faddbcac5f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupApiSchema]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbaf314391f581290f3072a95d25a25e5dd484a5b4f720a44473688c242fc36(
    *,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_object_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7b7157bd14ae4ee2155385836e57491c3c4f0e79d3f2bedd05af6526432a55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1e05dc1ccd185a5181c1bf91a25e01f8964bf4079ec30f19a7e9a5f38714a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc5e96f3ad1c7e09bad00129eeed66177623486b33a6e96431dc75d38cdac08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7904ee991b006ee04c2181d81a3ad07316aeb2ebb812270e84893f705bf8ae0c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101e199109dcb2762caaa0ecdb7d32871e4c30ccc1cc472e448264240405d83e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff2a20802da51e398928a30888c250ecbda3562d6d1adf8f739b2cf9ad3daf0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentAgentActionGroupApiSchemaS3]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30fd4afba5776ee854fc1d3024dee4eb5b4852e1bbbb6f253c26ffaee4d71b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77b59cad1035cb08209101cc46145c0e068040ea4d47b047d3f334b2f1de69b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967582586ab9a24e03654fc59c9eecef3de92d3957e0db1aab9c39c448abb002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d69a58b1d705db3edaa1d39ed4fb502898fd964b81cbc749d22b82e0a17826(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentAgentActionGroupApiSchemaS3]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a69bdaab037a4b0d06eaa2ecef933beb455ebca382db9b3ce756e3ad65fca7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action_group_name: builtins.str,
    agent_id: builtins.str,
    agent_version: builtins.str,
    action_group_executor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentAgentActionGroupActionGroupExecutor, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action_group_state: typing.Optional[builtins.str] = None,
    api_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentAgentActionGroupApiSchema, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    parent_action_group_signature: typing.Optional[builtins.str] = None,
    skip_resource_in_use_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
