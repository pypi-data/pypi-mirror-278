from typing import Required, TypedDict, Union


class GroupAttributesSnapshot(TypedDict, total=False):
    """
    group_attributes_snapshot.

    UUID:
      maxLength: 36
      minLength: 32
      type: string
    """

    group_deleted: Required[bool]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    group_id: Required[int]
    """ Required property """

    status: Required[int]
    """ Required property """

    substatus: Required[Union[int, None]]
    """ Required property """

    priority: Union[int, None]
    first_release_id: "_GroupattributessnapshotUuid"
    """
    minLength: 32
    maxLength: 36
    """

    first_seen: Required[str]
    """ Required property """

    num_comments: Required[int]
    """ Required property """

    assignee_user_id: Required[Union[int, None]]
    """ Required property """

    assignee_team_id: Required[Union[int, None]]
    """ Required property """

    owner_suspect_commit_user_id: Required[Union[int, None]]
    """ Required property """

    owner_ownership_rule_user_id: Required[Union[int, None]]
    """ Required property """

    owner_ownership_rule_team_id: Required[Union[int, None]]
    """ Required property """

    owner_codeowners_user_id: Required[Union[int, None]]
    """ Required property """

    owner_codeowners_team_id: Required[Union[int, None]]
    """ Required property """

    timestamp: Required[str]
    """ Required property """



_GroupattributessnapshotUuid = str
"""
minLength: 32
maxLength: 36
"""

