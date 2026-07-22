"""
SelfGPT — AI: Prompt Builder

Compiles an Identity's structured profile into a versioned system prompt.
Uses Jinja2 templates so identities are data, not code.

Layered prompt construction:
  Base Instructions → Personality Profile → Knowledge Context (RAG)
  → Memory Context → Custom Rules
"""

import logging
from typing import Dict, List, Optional

from jinja2 import Template

logger = logging.getLogger(__name__)

# ── System Prompt Template ──────────────────────────────────────────────
# This Jinja2 template compiles an IdentityProfile into a system prompt.
# It is the same for ALL identities — built-in and custom.

SYSTEM_PROMPT_TEMPLATE = Template("""\
You are {{ name }}. {{ tagline }}

## About You
{{ background_story }}

## Your Profession & Expertise
- Profession: {{ profession }}
{% if expertise %}- Expertise: {{ expertise | join(', ') }}{% endif %}
{% if domain_knowledge %}- Domain Knowledge: {{ domain_knowledge | join(', ') }}{% endif %}

## Your Personality
{% for trait, value in personality_traits.items() %}\
- {{ trait | capitalize }}: {{ (value * 100) | int }}%
{% endfor %}\

## Your Communication Style
- Speaking Style: {{ speaking_style }}
- Tone: {{ tone }}
- Response Length: {{ response_length }}
- Emoji Usage: {{ emoji_usage }}
- Reasoning Style: {{ reasoning_style }}
- Teaching Style: {{ teaching_style }}
{% if languages %}- Languages: {{ languages | join(', ') }}{% endif %}
{% if catchphrase %}- Catchphrase: "{{ catchphrase }}"{% endif %}

{% if values %}
## Your Values
{% for v in values %}- {{ v }}
{% endfor %}{% endif %}

{% if goals %}
## Your Goals
{% for g in goals %}- {{ g }}
{% endfor %}{% endif %}

{% if beliefs %}
## Your Beliefs
{% for b in beliefs %}- {{ b }}
{% endfor %}{% endif %}

{% if rules_restrictions %}
## Rules & Restrictions
{% for r in rules_restrictions %}- {{ r }}
{% endfor %}{% endif %}

{% if example_exchanges %}
## Example Conversations
{% for ex in example_exchanges %}
User: {{ ex.user }}
You: {{ ex.assistant }}
{% endfor %}{% endif %}

{% if memory_context %}
## What You Remember About This User
{{ memory_context }}
{% endif %}

{% if rag_context %}
## Relevant Knowledge
{{ rag_context }}
{% endif %}

## Important
{{ disclaimer }}

Stay in character at all times. Be helpful, engaging, and true to your personality.\
""")


def build_system_prompt(
    identity_data: Dict,
    memory_context: Optional[str] = None,
    rag_context: Optional[str] = None,
) -> str:
    """
    Compile an identity's profile + runtime context into a system prompt.

    Args:
        identity_data: Dict with keys from IdentityProfile + name, tagline, disclaimer
        memory_context: Formatted string of relevant memories
        rag_context: Formatted string of relevant RAG chunks with citations

    Returns:
        Compiled system prompt string.
    """
    profile = identity_data.get("profile", {})

    template_vars = {
        "name": identity_data.get("name", "AI Assistant"),
        "tagline": identity_data.get("tagline", ""),
        "background_story": profile.get("background_story", ""),
        "profession": profile.get("profession", ""),
        "expertise": profile.get("expertise", []),
        "domain_knowledge": profile.get("domain_knowledge", []),
        "personality_traits": profile.get("personality_traits", {}),
        "speaking_style": profile.get("speaking_style", "conversational"),
        "tone": profile.get("tone", "friendly"),
        "response_length": profile.get("response_length", "balanced"),
        "emoji_usage": profile.get("emoji_usage", "minimal"),
        "reasoning_style": profile.get("reasoning_style", "logical"),
        "teaching_style": profile.get("teaching_style", "socratic"),
        "languages": profile.get("languages", ["English"]),
        "catchphrase": profile.get("catchphrase"),
        "values": profile.get("values", []),
        "goals": profile.get("goals", []),
        "beliefs": profile.get("beliefs", []),
        "rules_restrictions": profile.get("rules_restrictions", []),
        "example_exchanges": profile.get("example_exchanges", []),
        "disclaimer": identity_data.get("disclaimer", ""),
        "memory_context": memory_context,
        "rag_context": rag_context,
    }

    return SYSTEM_PROMPT_TEMPLATE.render(**template_vars).strip()


def compile_identity_system_prompt(identity) -> str:
    """
    Convenience: compile a Beanie Identity document into a system prompt
    (without runtime memory/RAG context).
    """
    identity_dict = identity.model_dump()
    return build_system_prompt(identity_dict)
