from django.forms import BaseInlineFormSet


class ReadOnlyInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable formset empty forms
        self.can_delete = False
        for form in self.forms:
            form.empty_permitted = False

    def has_add_permission(self, request):
        return False
