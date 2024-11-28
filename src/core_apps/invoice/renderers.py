from rest_framework.renderers import JSONRenderer

class InvoiceJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'invoice'
    pagination_object_label = 'invoices'
    pagination_count_label = 'count'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, list):
            return super().render({
                self.pagination_object_label: data
            })
        return super().render({
            self.object_label: data
        })

class InvoicesJSONRenderer(InvoiceJSONRenderer):
    object_label = 'invoices'
