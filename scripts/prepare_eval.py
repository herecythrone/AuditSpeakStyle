#!/usr/bin/env python3
"""Export answer-free evaluation inputs; never invoke a model or overwrite a destination."""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prepare_eval(root: Path, out: Path) -> dict:
    """Copy an installable Skill and input-only cases into a NEW local directory."""
    if out.exists() or out.is_symlink():
        raise FileExistsError('destination exists; no overwrite is allowed')
    source = root / 'skills/audit-speak-style'
    if not (source / 'SKILL.md').is_file():
        raise ValueError('source Skill is missing')
    for p in source.rglob('*'):
        if p.is_symlink():
            raise ValueError('symlink is not allowed in exported Skill')
    required = [source/'PROVENANCE.md', source/'LICENSES/A-market-ecm-lawyer-plugin.txt']
    if any(not p.is_file() for p in required):
        raise ValueError('Skill provenance and upstream LICENSE must be present')
    data = json.loads((root / 'tests/cases.json').read_text(encoding='utf-8'))
    records, explicit, seen = [], [], set()
    cases = data['cases']
    for case in cases:
        cid, inp = case['id'], case['input']
        if not isinstance(cid,str) or cid in seen or not isinstance(inp,str) or not inp:
            raise ValueError('invalid or duplicate input fixture')
        if case.get('trigger') not in {'yes','no','partial'}:
            raise ValueError('invalid fixture trigger')
        seen.add(cid)
        row = {'id':cid, 'input':inp}
        records.append(row)
        if case['trigger'] in {'yes','partial'}:
            explicit.append(row)
    out.mkdir(parents=True,exist_ok=False)
    try:
        shutil.copytree(source,out/'skill/audit-speak-style')
        for name,rows in [('explicit-inputs.jsonl',explicit),('implicit-routing-inputs.jsonl',records)]:
            (out/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
        template = [{'id':c['id'],'model':'','host':'','run_time':'','invocation':'',
                     'actual_output':'','status':'not_run'} for c in cases]
        (out/'run-log-template.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in template),encoding='utf-8')
        (out/'README.md').write_text(
            '# 未运行的行为测试材料\n\n本目录只导出输入和技能，不调用模型。\n'
            'explicit-inputs包含写作或混合任务；显式加载技能后逐例运行。\n'
            'implicit-routing-inputs包含所有输入；用于宿主隐式路由，不先强制调用技能。\n'
            '每例使用独立上下文，只提供对应输入；不要提供仓库里的参考答案或验收条件。\n'
            '技能本身的教学案例与测试有重叠，因此不属于独立留出集或未见任务泛化测试。\n'
            '运行日志模板的not_run表示尚未运行；请记录真实输出，不填参考答案。\n',encoding='utf-8')
    except Exception:
        # Delete only the newly created directory. Existing destinations were rejected above.
        shutil.rmtree(out)
        raise
    return {'explicit_inputs':len(explicit),'implicit_inputs':len(records),'model_calls':0}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    try:
        print(json.dumps(prepare_eval(ROOT,args.out),ensure_ascii=False,sort_keys=True))
        print('Export only. No model or host behavior has been tested.')
        return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print('EXPORT ERROR: '+str(exc),file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
