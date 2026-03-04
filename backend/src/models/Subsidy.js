const mongoose = require('mongoose');

const subsidySchema = new mongoose.Schema({
  subsidyId: {
    type: String,
    unique: true,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  description: String,
  governmentBody: String,
  amount: Number,
  currency: {
    type: String,
    default: 'INR',
  },
  eligibilityCriteria: [String],
  applicableCrops: [String],
  applicableRegions: [String],
  applicationDeadline: Date,
  applicationLink: String,
  documentRequired: [String],
  beneficiaryCount: Number,
  allocatedBudget: Number,
  disbursed: Number,
  status: {
    type: String,
    enum: ['active', 'upcoming', 'closed', 'on_hold'],
    default: 'active',
  },
  contactPerson: String,
  contactPhone: String,
  contactEmail: String,
  lastUpdated: {
    type: Date,
    default: Date.now,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

const farmerSubsidyApplicationSchema = new mongoose.Schema({
  farmerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Farmer',
    required: true,
  },
  subsidyId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Subsidy',
    required: true,
  },
  applicationDate: {
    type: Date,
    default: Date.now,
  },
  status: {
    type: String,
    enum: ['submitted', 'under_review', 'approved', 'rejected', 'disbursed'],
    default: 'submitted',
  },
  documents: [{
    documentType: String,
    fileUrl: String,
    uploadDate: Date,
  }],
  approvalDate: Date,
  disbursementDate: Date,
  disbursementAmount: Number,
  remarks: String,
  updatedAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = {
  Subsidy: mongoose.model('Subsidy', subsidySchema),
  FarmerSubsidyApplication: mongoose.model('FarmerSubsidyApplication', farmerSubsidyApplicationSchema),
};
