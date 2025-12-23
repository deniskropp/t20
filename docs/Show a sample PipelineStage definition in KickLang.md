<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Show a sample PipelineStage definition in KickLang syntax

```kicklang
rolePlanner PLAN PipelineSample GranularityFine
  StageCollect storyrequest
  StagePlot 
    rolePlotWeaver FIND EntityEvents FilterPrecedesCurrent
    rolePlotWeaver LINK CurrentEvent precedes NextPlotPoint
  StageWorld 
    roleWorldBuilder CLUSTER EntitySetWorld FilterLocatedInCurrent worldstate
  StageNarrate 
    roleStoryteller SUMMARIZE plotpoint worldstate ToneEpic
  StageSynthesize 
    CLUSTER EntitySetUpdates ViewNarrative synthesisoutput
```

This sample defines a PipelineStage sequence within a PLAN block, chaining role actions across Collect-Plot-World-Narrate-Synthesize stages for story generation.[^1]

## Syntax Breakdown

Stages execute sequentially with role-specific verbs (FIND, LINK, CLUSTER, SUMMARIZE). Placebo pipes like storyrequest and worldstate pass context between stages.[^4][^1]

## Usage Notes

Copy-paste ready for Meta-AI Storybook workflows. Parameters like GranularityFine control resolution; ToneEpic customizes output style. Execution traces hierarchically per nested PLAN semantics.[^3][^1]
<span style="display:none">[^10][^11][^12][^13][^14][^2][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: kicklang-synthesis-objective-m-R_dnjarHQxOY8hblQMCb0A.md

[^2]: One-liner-about-KickLang.md

[^3]: this-is-solid-and-more-than-th-3FjwxRxoTDifMknLoT89qw.md

[^4]: Absolutely-lets-take-that-outline-and-turn-it-i.pdf

[^5]: https://www.jenkins.io/doc/book/pipeline/syntax/

[^6]: https://www.jenkins.io/doc/book/pipeline/

[^7]: https://gilesgas.github.io/jenkins.io/WEBSITE-461-update-imagesdir-references/doc/book/pipeline/syntax/

[^8]: https://www.mongodb.com/docs/drivers/csharp/v3.2/aggregation/stages/

[^9]: https://javadoc.jenkins.io/plugin/pipeline-graph-view/io/jenkins/plugins/pipelinegraphview/utils/PipelineStage.PipelineStageJsonProcessor.html

[^10]: https://javadoc.jenkins.io/plugin/pipeline-graph-view/io/jenkins/plugins/pipelinegraphview/utils/PipelineStage.html

[^11]: https://www.jenkins.io/doc/book/pipeline/development/

[^12]: https://devops.aibit.im/de/article/jenkins-pipeline-syntax-guide

[^13]: https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps/

[^14]: https://javadoc.jenkins.io/plugin/pipeline-model-definition/org/jenkinsci/plugins/pipeline/modeldefinition/model/Stages.html

