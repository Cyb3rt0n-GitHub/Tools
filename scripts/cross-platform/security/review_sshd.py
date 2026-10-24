"""Review saved sshd -T output offline; does not parse raw sshd_config or change services."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

# Review prompts, not a compliance baseline or proof of reachability.
PROMPTS = {
 'permitrootlogin': ('no', 'Review whether direct root SSH is required; preserve tested recovery access.'),
 'passwordauthentication': ('no', 'Review password-based access against the approved authentication design.'),
 'kbdinteractiveauthentication': ('no', 'Review interactive authentication and MFA/PAM requirements before any change.'),
 'permitemptypasswords': ('no', 'Review whether empty-password authentication could be accepted.'),
 'hostbasedauthentication': ('no', 'Review trust in client host identity and its approved use.'),
 'x11forwarding': ('no', 'Review whether X11 forwarding is required.'),
 'allowagentforwarding': ('no', 'Review agent forwarding requirements and credential exposure.'),
 'allowtcpforwarding': ('no', 'Review forwarding requirements, tunnels and administrative workflows.'),
 'gatewayports': ('no', 'Review remote forwarding bind policy and firewall controls.'),
 'permituserenvironment': ('no', 'Review user-supplied environment handling.'),
}
CONTEXT = ['authenticationmethods','usepam','pubkeyauthentication','allowusers','allowgroups',
           'denyusers','denygroups','listenaddress','port','maxauthtries','logingracetime','loglevel']


def review(data):
    values = {}
    for number, line in enumerate(data.decode('utf-8-sig').splitlines(),1):
        line = line.strip()
        if not line:
            continue
        parts = line.split(None,1)
        if len(parts) != 2 or parts[0] in ('Match','Include') or parts[0] != parts[0].lower():
            raise ValueError(f'Line {number}: expected effective sshd -T output, not source configuration')
        values.setdefault(parts[0],[]).append(parts[1])
    # Require markers normally emitted by extended-test output, avoiding empty/obviously partial input.
    if not all(k in values for k in ('port','permitrootlogin','passwordauthentication')):
        raise ValueError('Missing sshd -T markers; input may be incomplete or the wrong format')
    prompts=[]
    for key,(reference,note) in PROMPTS.items():
        observed=values.get(key,[])
        prompts.append({'setting':key,'observed':observed,'review_reference':reference,
                        'state':'unknown' if not observed else 'review' if observed != [reference] else 'matches_reference',
                        'note':note})
    return {'sha256':hashlib.sha256(data).hexdigest(),'review_prompts':prompts,
            'authentication_and_access_context':{k:values.get(k,[]) for k in CONTEXT},
            'effective_values':values}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input');p.add_argument('--context-label',required=True,
        help='Describe default or the exact simulated -C connection context; never include secrets')
    a=p.parse_args(argv)
    try:
        if not a.context_label.strip(): raise ValueError('Context label is required')
        result=review(Path(a.input).read_bytes())
        result.update(schema=1,generated_at=datetime.now(timezone.utc).isoformat(),context_label=a.context_label,
                      interpretation='Review aid only. Saved output does not prove running daemon configuration, successful authentication, MFA or network reachability. No remediation is performed.')
        print(json.dumps(result,indent=2))
        return 0
    except (OSError,ValueError) as exc:p.exit(2,f'Error: {exc}\n')


if __name__=='__main__':raise SystemExit(main())
