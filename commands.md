# Chief Productivity Officer (CPO) Discord Bot Commands

## Study Groups

- `/create_group <name> [max_size]`: Create a new study group
- `/join_group`: Join the existing study group
- `/leave_group`: Leave the current study group
- `/end_group`: End the current study group (group creator only)

## Pomodoro

- `/start_pomodoro [focus] [short_break] [long_break]`: Start a Pomodoro session
- `/end_pomodoro`: End the current Pomodoro session
- `/pause_pomodoro`: Pause the current Pomodoro session
- `/resume_pomodoro`: Resume the paused Pomodoro session

## Voice Channels

- `/create_vc [name] [visible]`: Create a voice channel for the study group
- `/delete_vc`: Delete the voice channel for the study group
- `/set_vc_cleanup_time <minutes>`: Set the time before empty voice channels are deleted
- `/set_vc_category <category>`: Set the category for study group voice channels
- `/vc_audit [days]`: Audit voice channel usage

## Task List

- `/task_add <description>`: Add a new task to your list
- `/task_complete <task_id>`: Mark a task as complete
- `/task_list`: List your current tasks

## Check-in

- `/checkin <duration> <mention>`: Start a check-in session
- `/checkin_channels <channels...>`: Set the channels where check-in commands can be used

## Management

- `/add_bot_developer <user>`: Add a bot developer (Bot Developer only)
- `/add_guild_manager <user>`: Add a guild manager (Bot Developer only)
- `/remove_guild_manager <user>`: Remove a guild manager (Bot Developer only)
- `/list_managers`: List all managers for this server

## Utility

- `/check_perms`: Check bot permissions in the current channel

Note: All commands use slash command syntax (/).