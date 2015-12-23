from .forms import UploadImageForm


class UploadImageMixin(object):
    def get_context_data(self, *args, **kwargs):
        context_data = super(UploadImageMixin, self).get_context_data(*args, **kwargs)
        context_data['image_form'] = UploadImageForm()
        return context_data


class OrderByMixin(object):
    ORDER_BY = 'o'

    @property
    def allowed_order_fields(self):
        raise NotImplementedError("Improperly Configured: You must specify allowed_order_fields property")

    def get_ordering(self):
        param = self.request.GET.get(self.ORDER_BY)
        if not param:
            return super(OrderByMixin, self).get_ordering()
        ordering = []
        none, pfx, name = param.rpartition('-')
        if name not in self.allowed_order_fields:
            return super(OrderByMixin, self).get_ordering()
        if name.startswith('-') and pfx == '-':
            ordering.append(name[1:])
        else:
            ordering.append(pfx + name)
        return ordering
