"""
Django management command to synchronize CELERY_BEAT_SCHEDULE with django_celery_beat database tables.
This command creates PeriodicTask objects in the database based on the CELERY_BEAT_SCHEDULE configuration.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from celery.schedules import crontab
import json


class Command(BaseCommand):
    help = "Synchronize CELERY_BEAT_SCHEDULE configuration with database tables"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing periodic tasks before creating new ones",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without actually creating tasks",
        )

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        clear_existing = options.get("clear", False)

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "DRY RUN MODE - No changes will be made to the database"
                )
            )

        # Clear existing tasks if requested
        if clear_existing and not dry_run:
            self.stdout.write("Clearing existing periodic tasks...")
            PeriodicTask.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Cleared all existing periodic tasks"))

        # Get the CELERY_BEAT_SCHEDULE from settings
        beat_schedule = getattr(settings, "CELERY_BEAT_SCHEDULE", {})

        if not beat_schedule:
            self.stdout.write(
                self.style.WARNING("No CELERY_BEAT_SCHEDULE found in settings")
            )
            return

        self.stdout.write(f"Found {len(beat_schedule)} tasks in CELERY_BEAT_SCHEDULE")

        tasks_created = 0
        tasks_updated = 0
        tasks_skipped = 0

        for task_name, task_config in beat_schedule.items():
            try:
                self.stdout.write(f"\nProcessing task: {task_name}")

                # Extract task configuration
                task_path = task_config["task"]
                schedule_config = task_config["schedule"]
                task_args = task_config.get("args", [])
                task_kwargs = task_config.get("kwargs", {})
                task_options = task_config.get("options", {})

                # Check if task already exists
                existing_task = PeriodicTask.objects.filter(name=task_name).first()

                if existing_task and not clear_existing:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Task '{task_name}' already exists, skipping..."
                        )
                    )
                    tasks_skipped += 1
                    continue

                # Create or get crontab schedule
                if isinstance(schedule_config, crontab):
                    crontab_schedule, created = CrontabSchedule.objects.get_or_create(
                        minute=schedule_config.minute,
                        hour=schedule_config.hour,
                        day_of_week=schedule_config.day_of_week,
                        day_of_month=schedule_config.day_of_month,
                        month_of_year=schedule_config.month_of_year,
                    )
                    schedule_type = "crontab"
                    schedule_obj = crontab_schedule

                    if dry_run:
                        self.stdout.write(
                            f"  Would create/use crontab: {crontab_schedule}"
                        )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f"  Unsupported schedule type for task '{task_name}'"
                        )
                    )
                    continue

                # Prepare task data
                task_data = {
                    "name": task_name,
                    "task": task_path,
                    "enabled": True,
                }

                # Set schedule
                if schedule_type == "crontab":
                    task_data["crontab"] = schedule_obj

                # Set args and kwargs
                if task_args:
                    task_data["args"] = json.dumps(task_args)
                if task_kwargs:
                    task_data["kwargs"] = json.dumps(task_kwargs)

                # Set queue and other options
                if "queue" in task_options:
                    task_data["queue"] = task_options["queue"]
                if "expires" in task_options:
                    # Convert expires to datetime if it's an integer (seconds)
                    expires_value = task_options["expires"]
                    if isinstance(expires_value, int):
                        from datetime import datetime, timedelta

                        task_data["expires"] = datetime.now() + timedelta(
                            seconds=expires_value
                        )
                    else:
                        task_data["expires"] = expires_value

                if dry_run:
                    self.stdout.write(f"  Would create periodic task:")
                    self.stdout.write(f"    Name: {task_name}")
                    self.stdout.write(f"    Task: {task_path}")
                    self.stdout.write(f"    Schedule: {schedule_obj}")
                    self.stdout.write(f"    Args: {task_args}")
                    self.stdout.write(f"    Kwargs: {task_kwargs}")
                    self.stdout.write(f"    Options: {task_options}")
                else:
                    # Create or update the periodic task
                    if existing_task:
                        for key, value in task_data.items():
                            setattr(existing_task, key, value)
                        existing_task.save()
                        tasks_updated += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"  Updated periodic task '{task_name}'")
                        )
                    else:
                        PeriodicTask.objects.create(**task_data)
                        tasks_created += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"  Created periodic task '{task_name}'")
                        )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"  Error processing task '{task_name}': {e}")
                )

        # Summary
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nDRY RUN SUMMARY: Would process {len(beat_schedule)} tasks"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nSUMMARY: Created {tasks_created}, Updated {tasks_updated}, Skipped {tasks_skipped} tasks"
                )
            )
            self.stdout.write(
                self.style.SUCCESS("Periodic tasks synchronized successfully!")
            )
            self.stdout.write(
                "You can now view the tasks in Django Admin under 'Periodic Tasks'"
            )
