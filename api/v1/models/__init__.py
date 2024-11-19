from .base import BaseTableModel
from .user import User
from .role import Role
from .project import Project
from .project_member import ProjectMember
from .invoice import Invoice
from .invoice_item import InvoiceItem

# from flask_principal import Permission, RoleNeed

# admin_permission = Permission(RoleNeed('Admin'))

# class CRUDMixin(object):
#     __table_args__ = {'extend_existing': True}

#     id = db.Column(db.Integer, primary_key=True)

#     @classmethod
#     def create(cls, commit=True, **kwargs):
#         instance = cls(**kwargs)
#         return instance.save(commit=commit)

#     @classmethod
#     def get(cls, id):
#         return cls.query.get(id)

#     # We will also proxy Flask-SqlAlchemy's get_or_44
#     # for symmetry
#     @classmethod
#     def get_or_404(cls, id):
#         return cls.query.get_or_404(id)

#     def update(self, commit=True, **kwargs):
#         for attr, value in kwargs.iteritems():
#             setattr(self, attr, value)
#         return commit and self.save() or self

#     def save(self, commit=True):
#         db.session.add(self)
#         if commit:
#             db.session.commit()
#         return self

#     def delete(self, commit=True):
#         db.session.delete(self)
#         return commit and db.session.commit()
