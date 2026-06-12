#!/usr/bin/env python3
import os
import sys
import json
import argparse
from pathlib import Path


def get_session_id():
    """获取 Trae sessionId"""
    session_id = os.environ.get("TRAE_SESSION_ID")
    if not session_id:
        print("错误: 未找到 TRAE_SESSION_ID 环境变量", file=sys.stderr)
        sys.exit(1)
    return session_id


def get_history_traces():
    """获取历史轨迹"""
    trae_home = os.environ.get("TRAE_HOME")
    if not trae_home:
        print("错误: 未找到 TRAE_HOME 环境变量", file=sys.stderr)
        sys.exit(1)

    history_dir = Path(trae_home) / "history"
    traces = []

    if history_dir.exists():
        for trace_file in sorted(history_dir.glob("*.json"), reverse=True):
            try:
                with open(trace_file, "r", encoding="utf-8") as f:
                    trace_data = json.load(f)
                    traces.append({
                        "file": trace_file.name,
                        "data": trace_data
                    })
            except Exception as e:
                print(f"警告: 无法读取 {trace_file}: {e}", file=sys.stderr)

    return traces


def get_current_conversation():
    """获取本轮对话"""
    trae_home = os.environ.get("TRAE_HOME")
    if not trae_home:
        print("错误: 未找到 TRAE_HOME 环境变量", file=sys.stderr)
        sys.exit(1)

    conversation_file = Path(trae_home) / "current_conversation.json"
    if conversation_file.exists():
        try:
            with open(conversation_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"警告: 无法读取当前对话文件: {e}", file=sys.stderr)
    
    return None


def main():
    parser = argparse.ArgumentParser(description="获取 Trae sessionId、历史轨迹和当前对话")
    parser.add_argument("--session", action="store_true", help="仅显示 sessionId")
    parser.add_argument("--history", action="store_true", help="仅显示历史轨迹")
    parser.add_argument("--current", action="store_true", help="仅显示当前对话")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()

    if args.session:
        session_id = get_session_id()
        if args.json:
            print(json.dumps({"sessionId": session_id}, ensure_ascii=False, indent=2))
        else:
            print(session_id)
    elif args.history:
        traces = get_history_traces()
        if args.json:
            print(json.dumps({"traces": traces}, ensure_ascii=False, indent=2))
        else:
            for i, trace in enumerate(traces, 1):
                print(f"\n=== 轨迹 {i}: {trace['file']} ===")
                print(json.dumps(trace["data"], ensure_ascii=False, indent=2))
    elif args.current:
        conversation = get_current_conversation()
        if args.json:
            print(json.dumps({"currentConversation": conversation}, ensure_ascii=False, indent=2))
        else:
            if conversation:
                print("=== 当前对话 ===")
                print(json.dumps(conversation, ensure_ascii=False, indent=2))
            else:
                print("未找到当前对话")
    else:
        session_id = get_session_id()
        traces = get_history_traces()
        conversation = get_current_conversation()
        output = {
            "sessionId": session_id,
            "traces": traces,
            "currentConversation": conversation
        }
        if args.json:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(f"Session ID: {session_id}")
            print(f"\n历史轨迹数量: {len(traces)}")
            for i, trace in enumerate(traces, 1):
                print(f"\n--- 轨迹 {i}: {trace['file']} ---")
                print(json.dumps(trace["data"], ensure_ascii=False, indent=2))
            if conversation:
                print(f"\n=== 当前对话 ===")
                print(json.dumps(conversation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
