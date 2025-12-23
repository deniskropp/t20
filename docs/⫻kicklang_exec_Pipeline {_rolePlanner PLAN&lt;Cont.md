<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# ⫻kicklang/exec

Pipeline {
rolePlanner PLAN<ContextArtifact, NarrativeArtifact> PipelineMain GranularityFine
Stage1Prep FIND EntityContext context
Stage2Nested roleSubPlanner PLAN<ContextArtifact, NarrativeArtifact> PipelineSub context
Stage3Synth SUMMARIZE PipelineSub output
}

**Pipeline Execution Initiated**

The KickLang `⫻kicklang/exec` command activates a nested planning pipeline for generating NarrativeArtifact from ContextArtifact using rolePlanner at fine granularity.[^1][^2]

## Stage1Prep: Context Discovery

rolePlanner executes FIND EntityContext to locate relevant context entities in the knowledge graph, pulling nodes like prior scenes, characters, or lore. This prepares structured input for nested planning without assumptions.[^2][^1]

## Stage2Nested: Sub-Pipeline Planning

roleSubPlanner launches PLAN<ContextArtifact, NarrativeArtifact> PipelineSub on the discovered context, chaining roles such as PlotWeaver for sequencing, WorldBuilder for consistency, and Storyteller for synthesis. GranularityFine ensures detailed, step-wise operations like LINK precedes or CLUSTER EntitySetWorld.[^1][^2]

## Stage3Synth: Output Synthesis

Final SUMMARIZE aggregates PipelineSub results into a cohesive NarrativeArtifact, applying TRANSFORM ViewProse for readable output while preserving graph updates (e.g., new edges like hastraitTensionRising). The pipeline yields traceable synthesisoutput ready for chaining.[^2][^1]
<span style="display:none">[^10][^11][^12][^13][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: kicklang-synthesis-objective-m-R_dnjarHQxOY8hblQMCb0A.md

[^2]: Absolutely-lets-take-that-outline-and-turn-it-i.pdf

[^3]: One-liner-about-KickLang.md

[^4]: https://www.jenkins.io/doc/book/pipeline/syntax/

[^5]: https://stackoverflow.com/questions/75848076/implement-pipeline-with-context-that-has-stages-without-context

[^6]: https://www.jenkins.io/doc/book/pipeline/

[^7]: https://www.reddit.com/r/devops/comments/l3w5ck/jenkins_declarative_pipeline/

[^8]: https://carson.math.uwm.edu/jenkins/job/clubb_ifort_debug_plot/pipeline-syntax/

[^9]: https://www.reddit.com/r/jenkinsci/comments/a94n7f/conditional_steps_inside_a_stage_of_declarative/

[^10]: https://docs.drone.io/yaml/exec/

[^11]: https://github.com/spinnaker/spinnaker/issues/2338

[^12]: https://github.com/tektoncd/pipeline/issues/168

[^13]: https://www.reddit.com/r/LangChain/comments/1hxeqev/how_to_summarize_large_documents/

