from django.contrib import admin

from users.models import (
    Domain,
    Follow,
    Identity,
    InboxMessage,
    Invite,
    PasswordReset,
    User,
    UserEvent,
)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["domain", "service_domain", "local", "blocked", "public"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "created", "last_seen", "admin", "moderator", "banned"]
    search_fields = ["email"]


@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ["id", "handle", "actor_uri", "state", "local"]
    list_filter = ["local"]
    raw_id_fields = ["users"]
    actions = ["force_update"]
    readonly_fields = ["actor_json"]
    search_fields = ["username", "name"]

    @admin.action(description="Force Update")
    def force_update(self, request, queryset):
        for instance in queryset:
            instance.transition_perform("outdated")

    @admin.display(description="ActivityPub JSON")
    def actor_json(self, instance):
        return instance.to_ap()

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["id", "source", "target", "state"]
    raw_id_fields = ["source", "target"]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created"]
    raw_id_fields = ["user"]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(InboxMessage)
class InboxMessageAdmin(admin.ModelAdmin):
    list_display = ["id", "state", "state_changed", "message_type", "message_actor"]
    search_fields = ["message"]
    actions = ["reset_state"]
    readonly_fields = ["state_changed"]

    @admin.action(description="Reset State")
    def reset_state(self, request, queryset):
        for instance in queryset:
            instance.transition_perform("received")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "token", "note"]
