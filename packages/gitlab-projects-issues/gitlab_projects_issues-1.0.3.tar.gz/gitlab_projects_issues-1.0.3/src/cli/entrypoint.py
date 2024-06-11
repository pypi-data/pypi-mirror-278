#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace
from enum import Enum
from typing import Dict, List, Optional

# Modules libraries
from gitlab.v4.objects import Project as GitLabProject

# Components
from ..features.gitlab import GitLabFeature
from ..types.milestones import MilestoneDescription
from ..types.statistics import AssigneeStatistics, MilestoneStatistics, TimesStatistics
from ..prints.colors import Colors
from ..system.platform import Platform

# Entrypoint class, pylint: disable=too-few-public-methods
class Entrypoint:

    # Enumerations
    Result = Enum('Result', ['SUCCESS', 'FINALIZE', 'ERROR', 'CRITICAL'])

    # CLI, pylint: disable=too-many-branches
    @staticmethod
    def cli(options: Namespace) -> Result:

        # Variables
        project: Optional[GitLabProject] = None

        # Header
        print(' ')

        # GitLab client
        gitlab = GitLabFeature(
            options.gitlab,
            options.token,
        )
        print(f'{Colors.BOLD} - GitLab host: '
              f'{Colors.GREEN}{gitlab.url}'
              f'{Colors.RESET}')
        Platform.flush()

        # GitLab path
        project = gitlab.project(options.path)
        print(f'{Colors.BOLD} - GitLab project: '
              f'{Colors.GREEN}{project.path_with_namespace}'
              f'{Colors.CYAN} ({project.description})'
              f'{Colors.RESET}')
        print(' ')
        Platform.flush()

        # Handle single project
        Entrypoint.project(
            options,
            gitlab,
            project.path_with_namespace,
        )

        # Result
        return Entrypoint.Result.SUCCESS

    # Project, pylint: disable=too-many-locals,too-many-statements
    @staticmethod
    def project(
        options: Namespace,
        gitlab: GitLabFeature,
        criteria: str,
    ) -> Result:

        # Variables
        milestone: MilestoneStatistics
        milestonesstatistics: Dict[str, MilestoneStatistics] = {}

        # Acquire project
        project = gitlab.project(criteria)

        # Show project details
        print(f'{Colors.BOLD} - GitLab project: '
              f'{Colors.YELLOW_LIGHT}{project.path_with_namespace} '
              f'{Colors.CYAN}({project.description})'
              f'{Colors.RESET}')
        Platform.flush()

        # Detect milestones
        if project.issues_enabled and options.milestones_statistics:

            # Issues without milestone
            if not options.milestone or options.milestone == 'None':
                milestonesstatistics[''] = MilestoneStatistics('Without milestone', )

            # Iterate through milestones
            for milestone_obj in sorted(
                    project.milestones.list(
                        get_all=True,
                        state='active' if options.exclude_closed_milestones else None,
                    ), key=lambda milestone: milestone.due_date, reverse=False):

                # Filter specific milestone
                if options.milestone and options.milestone != 'None' and options.milestone not in [
                        str(milestone_obj.id), milestone_obj.title
                ]:
                    continue

                # Issues with milestone
                milestonesstatistics[milestone_obj.id] = MilestoneStatistics(
                    milestone_obj.title, )
                milestonesstatistics[milestone_obj.id].assignees[''] = AssigneeStatistics(
                    'Without assignee', )

        # Handle milestones statistics
        if project.issues_enabled and options.milestones_statistics:

            # Iterate through issues
            for issue in project.issues.list(
                    get_all=True,
                    order_by='created_at',
                    sort='asc',
                    state='opened' if options.exclude_closed_issues else None,
            ):

                # Validate milestone ID
                milestone_id = issue.milestone['id'] if 'id' in issue.milestone else ''
                if milestone_id not in milestonesstatistics:
                    continue

                # Get milestone statistics
                milestone = milestonesstatistics[milestone_id]

                # Parse issue timings
                defaulted: bool = 'time_estimate' not in issue.time_stats(
                ) or issue.time_stats()['time_estimate'] == 0
                if not defaulted:
                    if issue.state != 'closed':
                        time_estimate = issue.time_stats()['time_estimate']
                        time_spent = issue.time_stats()['total_time_spent']
                    else:
                        time_estimate = issue.time_stats()['time_estimate']
                        time_spent = time_estimate
                else:
                    time_estimate = int(options.default_estimate) * 60 * 60
                    if issue.state != 'closed':
                        time_spent = 0
                    else:
                        time_spent = time_estimate

                # Handle milestone statistics
                milestone.issues_count += 1
                if not milestone.times.defaulted and defaulted:
                    milestone.times.defaulted = True
                milestone.times.estimates += time_estimate
                milestone.times.spent += time_spent

                # Prepare issue assignee
                assignee_id = issue.assignee[
                    'id'] if issue.assignee and 'id' in issue.assignee else ''
                if assignee_id not in milestone.assignees:
                    milestone.assignees[assignee_id] = AssigneeStatistics(
                        issue.assignee['name'], )

                # Handle assignee statistics
                milestone.assignees[assignee_id].issues_count += 1
                if not milestone.assignees[assignee_id].times.defaulted and defaulted:
                    milestone.assignees[assignee_id].times.defaulted = True
                milestone.assignees[assignee_id].times.estimates += time_estimate
                milestone.assignees[assignee_id].times.spent += time_spent

                # Dump issue object
                if options.dump:
                    print(' ')
                    print(issue.to_json())

        # Show milestones statistics
        if project.issues_enabled and options.milestones_statistics:

            # Create milestones statistics
            for milestone_id, milestone in milestonesstatistics.items():
                if not milestone.issues_count:
                    continue

                # Create milestone section
                outputs: List[str] = []
                outputs += ['']
                outputs += [f'# Milestone statistics - {milestone.title}']
                outputs += ['']

                # Create milestone table
                outputs += [
                    '| Assignees | Issues | Estimated | Spent | Remaining | Progress |'
                ]
                outputs += [
                    '|-----------|--------|-----------|-------|-----------|----------|'
                ]

                # Inject milestone table per assignee
                for _, assignee in milestone.assignees.items():
                    if not assignee.issues_count:
                        continue
                    times = assignee.times
                    outputs += [
                        f'| **{assignee.name}** '
                        f'| {assignee.issues_count} '
                        f'| {TimesStatistics.human(times.estimates, times.defaulted)} '
                        f'| {TimesStatistics.human(times.spent, times.defaulted)} '
                        f'| {TimesStatistics.human(times.remaining, times.defaulted)} '
                        f'| {times.progress()} '
                        f'|'
                    ]

                # Inject milestone table total
                times = milestone.times
                outputs += [
                    '| _**Total**_ '
                    f'| _{milestone.issues_count}_ '
                    f'| _{TimesStatistics.human(times.estimates, times.defaulted)}_ '
                    f'| _{TimesStatistics.human(times.spent, times.defaulted)}_ '
                    f'| {TimesStatistics.human(times.remaining, times.defaulted)} '
                    f'| _{times.progress()}_ '
                    '|'
                ]

                # Export to terminal
                for line in outputs:
                    print(f' {line}')

                # Export to milestone
                if milestone_id:
                    milestone_obj = project.milestones.get(milestone_id)
                    milestone_obj.description = MilestoneDescription.inject_statistics(
                        description=milestone_obj.description,
                        statistics='\n'.join(outputs),
                    )
                    milestone_obj.save()

        # Dump project object
        if options.dump:
            print(' ')
            print(project.to_json())

        # Footer
        print(' ')
        Platform.flush()

        # Result
        return Entrypoint.Result.SUCCESS
