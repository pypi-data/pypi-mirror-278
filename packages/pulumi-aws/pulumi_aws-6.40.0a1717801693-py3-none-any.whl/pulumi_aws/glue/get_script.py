# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetScriptResult',
    'AwaitableGetScriptResult',
    'get_script',
    'get_script_output',
]

@pulumi.output_type
class GetScriptResult:
    """
    A collection of values returned by getScript.
    """
    def __init__(__self__, dag_edges=None, dag_nodes=None, id=None, language=None, python_script=None, scala_code=None):
        if dag_edges and not isinstance(dag_edges, list):
            raise TypeError("Expected argument 'dag_edges' to be a list")
        pulumi.set(__self__, "dag_edges", dag_edges)
        if dag_nodes and not isinstance(dag_nodes, list):
            raise TypeError("Expected argument 'dag_nodes' to be a list")
        pulumi.set(__self__, "dag_nodes", dag_nodes)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if language and not isinstance(language, str):
            raise TypeError("Expected argument 'language' to be a str")
        pulumi.set(__self__, "language", language)
        if python_script and not isinstance(python_script, str):
            raise TypeError("Expected argument 'python_script' to be a str")
        pulumi.set(__self__, "python_script", python_script)
        if scala_code and not isinstance(scala_code, str):
            raise TypeError("Expected argument 'scala_code' to be a str")
        pulumi.set(__self__, "scala_code", scala_code)

    @property
    @pulumi.getter(name="dagEdges")
    def dag_edges(self) -> Sequence['outputs.GetScriptDagEdgeResult']:
        return pulumi.get(self, "dag_edges")

    @property
    @pulumi.getter(name="dagNodes")
    def dag_nodes(self) -> Sequence['outputs.GetScriptDagNodeResult']:
        return pulumi.get(self, "dag_nodes")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def language(self) -> Optional[str]:
        return pulumi.get(self, "language")

    @property
    @pulumi.getter(name="pythonScript")
    def python_script(self) -> str:
        """
        Python script generated from the DAG when the `language` argument is set to `PYTHON`.
        """
        return pulumi.get(self, "python_script")

    @property
    @pulumi.getter(name="scalaCode")
    def scala_code(self) -> str:
        """
        Scala code generated from the DAG when the `language` argument is set to `SCALA`.
        """
        return pulumi.get(self, "scala_code")


class AwaitableGetScriptResult(GetScriptResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetScriptResult(
            dag_edges=self.dag_edges,
            dag_nodes=self.dag_nodes,
            id=self.id,
            language=self.language,
            python_script=self.python_script,
            scala_code=self.scala_code)


def get_script(dag_edges: Optional[Sequence[pulumi.InputType['GetScriptDagEdgeArgs']]] = None,
               dag_nodes: Optional[Sequence[pulumi.InputType['GetScriptDagNodeArgs']]] = None,
               language: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetScriptResult:
    """
    Use this data source to generate a Glue script from a Directed Acyclic Graph (DAG).

    ## Example Usage

    ### Generate Python Script

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.glue.get_script(language="PYTHON",
        dag_edges=[
            aws.glue.GetScriptDagEdgeArgs(
                source="datasource0",
                target="applymapping1",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="applymapping1",
                target="selectfields2",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="selectfields2",
                target="resolvechoice3",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="resolvechoice3",
                target="datasink4",
            ),
        ],
        dag_nodes=[
            aws.glue.GetScriptDagNodeArgs(
                id="datasource0",
                node_type="DataSource",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{source['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{source_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="applymapping1",
                node_type="ApplyMapping",
                args=[aws.glue.GetScriptDagNodeArgArgs(
                    name="mapping",
                    value="[(\\"column1\\", \\"string\\", \\"column1\\", \\"string\\")]",
                )],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="selectfields2",
                node_type="SelectFields",
                args=[aws.glue.GetScriptDagNodeArgArgs(
                    name="paths",
                    value="[\\"column1\\"]",
                )],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="resolvechoice3",
                node_type="ResolveChoice",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="choice",
                        value="\\"MATCH_CATALOG\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{destination['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{destination_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="datasink4",
                node_type="DataSink",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{destination['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{destination_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
        ])
    pulumi.export("pythonScript", example.python_script)
    ```

    ### Generate Scala Code

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.glue.get_script(language="SCALA",
        dag_edges=[
            aws.glue.GetScriptDagEdgeArgs(
                source="datasource0",
                target="applymapping1",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="applymapping1",
                target="selectfields2",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="selectfields2",
                target="resolvechoice3",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="resolvechoice3",
                target="datasink4",
            ),
        ],
        dag_nodes=[
            aws.glue.GetScriptDagNodeArgs(
                id="datasource0",
                node_type="DataSource",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{source['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{source_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="applymapping1",
                node_type="ApplyMapping",
                args=[aws.glue.GetScriptDagNodeArgArgs(
                    name="mappings",
                    value="[(\\"column1\\", \\"string\\", \\"column1\\", \\"string\\")]",
                )],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="selectfields2",
                node_type="SelectFields",
                args=[aws.glue.GetScriptDagNodeArgArgs(
                    name="paths",
                    value="[\\"column1\\"]",
                )],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="resolvechoice3",
                node_type="ResolveChoice",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="choice",
                        value="\\"MATCH_CATALOG\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{destination['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{destination_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="datasink4",
                node_type="DataSink",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{destination['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{destination_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
        ])
    pulumi.export("scalaCode", example.scala_code)
    ```


    :param Sequence[pulumi.InputType['GetScriptDagEdgeArgs']] dag_edges: List of the edges in the DAG. Defined below.
    :param Sequence[pulumi.InputType['GetScriptDagNodeArgs']] dag_nodes: List of the nodes in the DAG. Defined below.
    :param str language: Programming language of the resulting code from the DAG. Defaults to `PYTHON`. Valid values are `PYTHON` and `SCALA`.
    """
    __args__ = dict()
    __args__['dagEdges'] = dag_edges
    __args__['dagNodes'] = dag_nodes
    __args__['language'] = language
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:glue/getScript:getScript', __args__, opts=opts, typ=GetScriptResult).value

    return AwaitableGetScriptResult(
        dag_edges=pulumi.get(__ret__, 'dag_edges'),
        dag_nodes=pulumi.get(__ret__, 'dag_nodes'),
        id=pulumi.get(__ret__, 'id'),
        language=pulumi.get(__ret__, 'language'),
        python_script=pulumi.get(__ret__, 'python_script'),
        scala_code=pulumi.get(__ret__, 'scala_code'))


@_utilities.lift_output_func(get_script)
def get_script_output(dag_edges: Optional[pulumi.Input[Sequence[pulumi.InputType['GetScriptDagEdgeArgs']]]] = None,
                      dag_nodes: Optional[pulumi.Input[Sequence[pulumi.InputType['GetScriptDagNodeArgs']]]] = None,
                      language: Optional[pulumi.Input[Optional[str]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetScriptResult]:
    """
    Use this data source to generate a Glue script from a Directed Acyclic Graph (DAG).

    ## Example Usage

    ### Generate Python Script

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.glue.get_script(language="PYTHON",
        dag_edges=[
            aws.glue.GetScriptDagEdgeArgs(
                source="datasource0",
                target="applymapping1",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="applymapping1",
                target="selectfields2",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="selectfields2",
                target="resolvechoice3",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="resolvechoice3",
                target="datasink4",
            ),
        ],
        dag_nodes=[
            aws.glue.GetScriptDagNodeArgs(
                id="datasource0",
                node_type="DataSource",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{source['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{source_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="applymapping1",
                node_type="ApplyMapping",
                args=[aws.glue.GetScriptDagNodeArgArgs(
                    name="mapping",
                    value="[(\\"column1\\", \\"string\\", \\"column1\\", \\"string\\")]",
                )],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="selectfields2",
                node_type="SelectFields",
                args=[aws.glue.GetScriptDagNodeArgArgs(
                    name="paths",
                    value="[\\"column1\\"]",
                )],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="resolvechoice3",
                node_type="ResolveChoice",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="choice",
                        value="\\"MATCH_CATALOG\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{destination['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{destination_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="datasink4",
                node_type="DataSink",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{destination['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{destination_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
        ])
    pulumi.export("pythonScript", example.python_script)
    ```

    ### Generate Scala Code

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.glue.get_script(language="SCALA",
        dag_edges=[
            aws.glue.GetScriptDagEdgeArgs(
                source="datasource0",
                target="applymapping1",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="applymapping1",
                target="selectfields2",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="selectfields2",
                target="resolvechoice3",
            ),
            aws.glue.GetScriptDagEdgeArgs(
                source="resolvechoice3",
                target="datasink4",
            ),
        ],
        dag_nodes=[
            aws.glue.GetScriptDagNodeArgs(
                id="datasource0",
                node_type="DataSource",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{source['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{source_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="applymapping1",
                node_type="ApplyMapping",
                args=[aws.glue.GetScriptDagNodeArgArgs(
                    name="mappings",
                    value="[(\\"column1\\", \\"string\\", \\"column1\\", \\"string\\")]",
                )],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="selectfields2",
                node_type="SelectFields",
                args=[aws.glue.GetScriptDagNodeArgArgs(
                    name="paths",
                    value="[\\"column1\\"]",
                )],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="resolvechoice3",
                node_type="ResolveChoice",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="choice",
                        value="\\"MATCH_CATALOG\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{destination['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{destination_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
            aws.glue.GetScriptDagNodeArgs(
                id="datasink4",
                node_type="DataSink",
                args=[
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="database",
                        value=f"\\"{destination['name']}\\"",
                    ),
                    aws.glue.GetScriptDagNodeArgArgs(
                        name="table_name",
                        value=f"\\"{destination_aws_glue_catalog_table['name']}\\"",
                    ),
                ],
            ),
        ])
    pulumi.export("scalaCode", example.scala_code)
    ```


    :param Sequence[pulumi.InputType['GetScriptDagEdgeArgs']] dag_edges: List of the edges in the DAG. Defined below.
    :param Sequence[pulumi.InputType['GetScriptDagNodeArgs']] dag_nodes: List of the nodes in the DAG. Defined below.
    :param str language: Programming language of the resulting code from the DAG. Defaults to `PYTHON`. Valid values are `PYTHON` and `SCALA`.
    """
    ...
