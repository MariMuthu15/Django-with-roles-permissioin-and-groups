from django.db.models.signals import post_save, post_migrate
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver
import logging


logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def assign_superuser_group(sender, instance=None, created=False, **kwargs):
    if created and instance.is_superuser:
        logger.info(f"Creating superuser: {instance.username}")
        
        try:
            group, group_created = Group.objects.get_or_create(name='SuperAdmin')
            
            # Always ensure group has all current permissions
            ensure_superadmin_has_all_permissions(group)
            
            # Add user to the group
            instance.groups.add(group)
            logger.info(f"Added user {instance.username} to SuperAdmin group")
            
        except Exception as e:
            logger.error(f"Error assigning superuser group to {instance.username}: {e}")


def create_superadmin_group(sender, **kwargs):
    """
    Create SuperAdmin group with all permissions after migrations.
    This runs EVERY time migrations are run, ensuring new permissions are added.
    """
    logger.info("Running create_superadmin_group signal")
    
    try:
        group, created = Group.objects.get_or_create(name='SuperAdmin')
        logger.info(f"SuperAdmin group {'created' if created else 'already exists'}")
        
        ensure_superadmin_has_all_permissions(group)
        
    except Exception as e:
        logger.error(f"Error in create_superadmin_group: {e}")


def ensure_superadmin_has_all_permissions(group):
    """
    Utility function to ensure SuperAdmin group has ALL available permissions.
    This handles both new permissions and existing ones.
    """
    all_permissions = Permission.objects.all()
    
    if all_permissions.exists():
        current_perms = group.permissions.count()
        total_perms = all_permissions.count()
        
        if current_perms != total_perms:
            # Group doesn't have all permissions, update it
            group.permissions.set(all_permissions)
            logger.info(f"Updated SuperAdmin group: {current_perms} -> {total_perms} permissions")
        else:
            logger.info(f"SuperAdmin group already has all {total_perms} permissions")
    else:
        logger.warning("No permissions found in database")
        