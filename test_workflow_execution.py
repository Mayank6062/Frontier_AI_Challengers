#!/usr/bin/env python
"""Test script to verify complete workflow execution end-to-end."""

import asyncio
import json
from backend.di.composition import DIContainer
from backend.orchestration.models import WorkflowContext, StageDefinition
from backend.core.engagement.engagement_repository import EngagementRepository
from backend.core.engagement.engagement_manager import EngagementManager
from backend.core.interfaces.storage_interface import StorageInterface
from typing import cast


async def test_workflow_execution():
    """Test the complete workflow execution pipeline."""
    print("\n" + "="*80)
    print("WORKFLOW EXECUTION END-TO-END TEST")
    print("="*80 + "\n")
    
    # Step 1: Initialize DI Container
    print("Step 1: Initialize DI Container")
    print("-" * 40)
    di = DIContainer()
    provided = di.build()
    print(f"✓ DI Container initialized")
    print(f"✓ Registered agents: {len(list(provided.agent_registry.list()))}")
    print()
    
    # Step 2: Create Engagement
    print("Step 2: Create Engagement")
    print("-" * 40)
    engagement_repo = EngagementRepository(
        cast(StorageInterface, provided.storage)
    )
    engagement_mgr = EngagementManager(engagement_repo)
    engagement = engagement_mgr.create(
        title="Microservices Architecture",
        description="Design a microservices architecture for a real-time collaboration platform"
    )
    print(f"✓ Engagement created: {engagement.id}")
    print(f"  Title: {engagement.title}")
    print(f"  Description: {engagement.description}")
    print()
    
    # Step 3: Build Workflow Context
    print("Step 3: Build Workflow Context")
    print("-" * 40)
    ctx = WorkflowContext(
        engagement_id=engagement.id,
        input_payload={
            "user_message": "Design a microservices architecture for a real-time collaboration platform",
            "session_id": "test_session_123",
            "message_id": "msg_123",
        }
    )
    print(f"✓ WorkflowContext created")
    print(f"  Engagement ID: {ctx.engagement_id}")
    print(f"  Input payload keys: {list(ctx.input_payload.keys())}")
    print()
    
    # Step 4: Get Pipeline Definition
    print("Step 4: Get Pipeline Definition")
    print("-" * 40)
    pipeline_plan = provided.pipeline_manager.build_execution_plan()
    print(f"✓ Execution plan retrieved")
    print(f"  Stage groups: {pipeline_plan.stage_groups}")
    for i, group in enumerate(pipeline_plan.stage_groups):
        print(f"  Group {i}: {group}")
        for stage_id in group:
            stage_def = provided.pipeline_manager.get_stage_definition(stage_id)
            print(f"    - {stage_id}: agent={stage_def.agent_id}, required={stage_def.required}")
    print()
    
    # Step 5: Execute Workflow
    print("Step 5: Execute Workflow")
    print("-" * 40)
    
    checkpoints = []
    def checkpoint_writer(eid, group, results):
        checkpoint_info = {
            "engagement_id": eid,
            "stage_group": group,
            "results": []
        }
        for r in results:
            checkpoint_info["results"].append({
                "stage_id": r.stage_id,
                "status": r.status.value,
                "error": r.error,
                "output_keys": list(r.output.keys()) if r.output else [],
            })
        checkpoints.append(checkpoint_info)
        print(f"  ✓ Checkpoint: Group {group}")
        for r in results:
            print(f"    - {r.stage_id}: {r.status.value}")
            if r.output:
                print(f"      Output keys: {list(r.output.keys())}")
            if r.error:
                print(f"      Error: {r.error}")
    
    print("  Running orchestrator.run_phase()...")
    results = await provided.master_orchestrator.run_phase(ctx, checkpoint_writer)
    print(f"✓ Workflow execution completed")
    print(f"  Total results: {len(results)}")
    print()
    
    # Step 6: Analyze Results
    print("Step 6: Analyze Results")
    print("-" * 40)
    print(f"  Accumulated context keys: {list(ctx.accumulated.keys())}")
    for stage_id, output in ctx.accumulated.items():
        if stage_id != "_meta":
            print(f"    - {stage_id}: {type(output).__name__}")
            if isinstance(output, dict):
                print(f"      Keys: {list(output.keys())}")
    
    print("\n  Detailed Results:")
    for i, result in enumerate(results):
        status_icon = "✓" if result.status.value == "SUCCESS" else "✗"
        print(f"    {status_icon} [{i}] {result.stage_id}: {result.status.value}")
        if result.output:
            print(f"          Output: {result.output}")
        if result.error:
            print(f"          Error: {result.error}")
        if result.errors:
            print(f"          Errors: {result.errors}")
        if result.confidence is not None:
            print(f"          Confidence: {result.confidence}")
    
    if "_meta" in ctx.accumulated:
        meta = ctx.accumulated["_meta"]
        if "confidences" in meta:
            print(f"\n  Confidences: {meta['confidences']}")
        if "errors" in meta and meta["errors"]:
            print(f"  Errors: {meta['errors']}")
    print()
    
    # Step 7: Summary
    print("Step 7: Summary")
    print("-" * 40)
    print(f"✓ Engagement ID: {engagement.id}")
    print(f"✓ Total Checkpoints: {len(checkpoints)}")
    print(f"✓ Total Results: {len(results)}")
    
    success_count = sum(1 for r in results if r.status.value == "SUCCESS")
    failed_count = sum(1 for r in results if r.status.value == "FAILED")
    print(f"✓ Success: {success_count}, Failed: {failed_count}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80 + "\n")
    
    return {
        "engagement_id": engagement.id,
        "results": len(results),
        "checkpoints": len(checkpoints),
        "success": success_count,
        "failed": failed_count,
    }


if __name__ == "__main__":
    result = asyncio.run(test_workflow_execution())
    print(json.dumps(result, indent=2))
