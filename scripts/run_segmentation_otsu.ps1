param(
  [Parameter(Mandatory = $true)]
  [string]$DatasetRoot,

  [Parameter(Mandatory = $true)]
  [string]$OutputRoot,

  [int]$ShardIndex = 0,
  [int]$ShardCount = 1,
  [int]$MaxDim = 1024,
  [string]$RunId = $null,
  [switch]$SkipIfPresent
)

$ErrorActionPreference = "Stop"

$argsList = @(
  "-m", "pipeline.sagemaker.segmentation_otsu_job",
  "--dataset-root", $DatasetRoot,
  "--output-root", $OutputRoot,
  "--shard-index", "$ShardIndex",
  "--shard-count", "$ShardCount",
  "--max-dim", "$MaxDim"
)

if ($RunId) {
  $argsList += @("--run-id", $RunId)
}
if ($SkipIfPresent) {
  $argsList += @("--skip-if-present")
}

python @argsList

