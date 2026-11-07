from datetime import datetime
from backend.extensions import db
from enum import Enum

class FarmRole(Enum):
    OWNER = "owner"
    MANAGER = "manager"
    WORKER = "worker"
    VIEWER = "viewer"

class Farm(db.Model):
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255), nullable=False)
    acreage = db.Column(db.Float)
    
    # Metadata as JSON
    soil_details = db.Column(db.Text) # e.g., {"type": "Loamy", "pH": 6.5}
    
    # Predictive Harvest Velocity (L3-1560)
    harvest_readiness_index = db.Column(db.Float, default=0.0) # 0-100%
    predicted_yield_volume = db.Column(db.Float, default=0.0) # Estimated kg
    last_velocity_update = db.Column(db.DateTime)
    
    # Regenerative Carbon Tracking (L3-1632)
    is_no_till = db.Column(db.Boolean, default=False)            # No-tillage practice
    cover_crop_active = db.Column(db.Boolean, default=False)      # Cover cropping in rotation
    organic_certified = db.Column(db.Boolean, default=False)      # Certified organic (no synthetic)
    sequestration_tier = db.Column(db.String(20), default='TIER_1') # TIER_1 to TIER_4
    total_carbon_credits_minted = db.Column(db.Float, default=0.0) # Lifetime credits earned
    
    # Regional Yield Prophet (L3-1635)
    spatial_grid_id = db.Column(db.Integer, db.ForeignKey('spatial_yield_grids.id'))
    
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('FarmMember', backref='farm', lazy='dynamic', cascade='all, delete-orphan')
    assets = db.relationship('FarmAsset', backref='farm', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'acreage': self.acreage,
            'soil_details': json.loads(self.soil_details) if self.soil_details else {},
            'member_count': self.members.count(),
            'created_at': self.created_at.isoformat()
        }

class FarmMember(db.Model):
    __tablename__ = 'farm_members'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    role = db.Column(db.String(20), default=FarmRole.WORKER.value)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Track who invited them
    invited_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'user_id': self.user_id,
            'role': self.role,
            'joined_at': self.joined_at.isoformat()
        }

class FarmAsset(db.Model):
    __tablename__ = 'farm_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=True)

    # Fields used by the asset health and maintenance API.
    asset_id = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    asset_type = db.Column(db.String(100), default='unknown')
    asset_name = db.Column(db.String(200))
    manufacturer = db.Column(db.String(100))
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    purchase_price = db.Column(db.Float)
    status = db.Column(db.String(30), default='ACTIVE')
    health_score = db.Column(db.Float, default=100.0)
    alert_threshold_days = db.Column(db.Integer, default=7)
    total_runtime_hours = db.Column(db.Float, default=0.0)
    last_telemetry = db.Column(db.Text)
    predicted_days_to_failure = db.Column(db.Integer)
    last_maintenance_date = db.Column(db.DateTime)
    next_maintenance_due = db.Column(db.DateTime)
    
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) # e.g., Tractor, Irrigation Pump, Storehouse
    purchase_value = db.Column(db.Float)
    purchase_date = db.Column(db.DateTime)
    
    condition = db.Column(db.String(50), default='Good') # 'Good', 'Needs Repair', 'Critical'
    last_maintenance = db.Column(db.DateTime)
    
    # Depreciated value tracker
    current_valuation = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'user_id': self.user_id,
            'farm_id': self.farm_id,
            'asset_type': self.asset_type or self.category,
            'asset_name': self.asset_name or self.name,
            'name': self.name or self.asset_name,
            'category': self.category or self.asset_type,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'serial_number': self.serial_number,
            'purchase_value': self.purchase_value or self.purchase_price,
            'purchase_price': self.purchase_price or self.purchase_value,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'condition': self.condition,
            'status': self.status,
            'health_score': self.health_score,
            'alert_threshold_days': self.alert_threshold_days,
            'total_runtime_hours': self.total_runtime_hours,
            'predicted_days_to_failure': self.predicted_days_to_failure,
            'next_maintenance_due': self.next_maintenance_due.isoformat() if self.next_maintenance_due else None,
            'current_valuation': self.current_valuation,
            'last_maintenance': self.last_maintenance.isoformat() if self.last_maintenance else None
        }


class MaintenanceLog(db.Model):
    """Maintenance history for a tracked farm asset."""
    __tablename__ = 'maintenance_logs'

    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.String(80), unique=True, nullable=False, index=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('farm_assets.id'), nullable=False, index=True)
    maintenance_type = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    parts_replaced = db.Column(db.Text, default='[]')
    cost = db.Column(db.Float, default=0.0)
    pre_maintenance_health = db.Column(db.Float)
    post_maintenance_health = db.Column(db.Float)
    technician_name = db.Column(db.String(200))
    technician_notes = db.Column(db.Text)
    scheduled_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    status = db.Column(db.String(30), default='SCHEDULED')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    asset = db.relationship('FarmAsset', backref=db.backref('maintenance_logs', lazy='dynamic'))
