# Terms of Service Creation & Review System

## Slash Command: `/terms-of-service`

### Description
Comprehensive terms of service creation and review system with specialized sub-agents for legal compliance and best practices.

### Usage
```
/terms-of-service [action] [options]
```

### Actions
- `create` - Create new terms of service from scratch
- `review` - Review existing terms of service
- `update` - Update existing terms to meet new requirements
- `audit` - Comprehensive compliance audit

### Options
- `--type` - Service type (saas, mobile-app, ecommerce, marketplace, api)
- `--jurisdiction` - Primary jurisdiction (us, eu, jp, global)
- `--compliance` - Specific compliance requirements (gdpr, ccpa, coppa, pci-dss)
- `--language` - Document language (en, ja, etc.)
- `--industry` - Industry-specific requirements (fintech, healthcare, education)

### Examples
```bash
/terms-of-service create --type saas --jurisdiction global --compliance gdpr,ccpa
/terms-of-service review --file ./terms.md --compliance gdpr
/terms-of-service audit --comprehensive
```

## Sub-Agents

### 1. Legal Compliance Agent (`legal-compliance-reviewer`)
**Purpose**: Ensures compliance with international and regional laws

**Specializations**:
- GDPR (EU) compliance verification
- CCPA/CPRA (California) compliance
- COPPA (Children's privacy) compliance
- PIPEDA (Canada) compliance
- LGPD (Brazil) compliance
- DPDP Act (India) compliance
- Cross-border data transfer requirements
- Industry-specific regulations (HIPAA, PCI-DSS, etc.)

**Key Functions**:
- Verify mandatory disclosure requirements
- Check consent mechanisms
- Validate data retention policies
- Ensure proper breach notification procedures
- Verify age verification requirements
- Check international data transfer clauses

### 2. Privacy & Data Protection Agent (`privacy-data-specialist`)
**Purpose**: Reviews and ensures comprehensive data protection measures

**Specializations**:
- Data collection scope definition
- Purpose limitation validation
- Data minimization principles
- User rights implementation
- Cookie and tracking policies
- Third-party data sharing agreements
- Data retention and deletion policies
- Security measures documentation

**Key Functions**:
- Audit data inventory requirements
- Verify opt-in/opt-out mechanisms
- Review data portability provisions
- Check encryption requirements
- Validate anonymization practices
- Ensure proper data subject rights

### 3. Risk & Liability Agent (`risk-liability-assessor`)
**Purpose**: Manages risk allocation and liability limitations

**Specializations**:
- Limitation of liability clauses
- Indemnification provisions
- Warranty disclaimers
- Insurance requirements
- Force majeure clauses
- Dispute resolution mechanisms
- Jurisdiction and governing law
- Class action waivers

**Key Functions**:
- Assess liability cap appropriateness
- Review indemnification balance
- Validate warranty disclaimers
- Check arbitration clauses
- Ensure proper risk allocation
- Verify enforceability in target jurisdictions

### 4. User Rights & Accessibility Agent (`user-rights-advocate`)
**Purpose**: Ensures user rights protection and document accessibility

**Specializations**:
- Consumer rights implementation
- Accessibility standards (WCAG)
- Plain language requirements
- Transparency obligations
- User control mechanisms
- Account termination procedures
- Data portability rights
- Complaint handling processes

**Key Functions**:
- Verify right to access implementation
- Check deletion request procedures
- Review modification rights
- Ensure clear cancellation policies
- Validate refund policies
- Check language clarity (grade level analysis)

### 5. Technical Integration Agent (`technical-integration-specialist`)
**Purpose**: Handles technical aspects and API/service integration

**Specializations**:
- API terms and rate limits
- SLA (Service Level Agreement) terms
- Uptime guarantees
- Technical support provisions
- Integration requirements
- Version control and updates
- Backward compatibility
- Technical documentation requirements

**Key Functions**:
- Define API usage restrictions
- Set rate limiting policies
- Establish SLA metrics
- Document technical requirements
- Specify integration guidelines
- Define update procedures

### 6. Intellectual Property Agent (`ip-protection-expert`)
**Purpose**: Manages intellectual property rights and content policies

**Specializations**:
- Copyright provisions
- Trademark usage
- Patent considerations
- Trade secret protection
- User-generated content rights
- License grants
- DMCA compliance
- Content moderation policies

**Key Functions**:
- Define IP ownership
- Establish licensing terms
- Set content usage rights
- Implement DMCA procedures
- Verify trademark policies
- Review user content licenses

### 7. Commercial Terms Agent (`commercial-terms-negotiator`)
**Purpose**: Handles pricing, payment, and commercial aspects

**Specializations**:
- Pricing and payment terms
- Subscription models
- Refund and cancellation policies
- Auto-renewal provisions
- Free trial terms
- Usage-based billing
- Currency and tax provisions
- Payment processing terms

**Key Functions**:
- Structure pricing tiers
- Define billing cycles
- Set refund conditions
- Establish renewal terms
- Verify payment security
- Define usage metrics

### 8. Compliance Audit Agent (`compliance-auditor`)
**Purpose**: Performs comprehensive compliance audits

**Specializations**:
- Regulatory compliance checking
- Policy consistency verification
- Cross-reference validation
- Update tracking
- Compliance reporting
- Gap analysis
- Best practice benchmarking
- Industry standard alignment

**Key Functions**:
- Run compliance checklists
- Generate audit reports
- Track policy versions
- Monitor regulatory changes
- Perform gap analysis
- Benchmark against competitors

## Workflow

### Creation Workflow
1. **Initial Assessment** (All agents collaborate)
   - Gather requirements
   - Identify applicable laws
   - Determine risk profile

2. **Drafting Phase**
   - Legal Compliance Agent creates framework
   - Privacy Agent adds data provisions
   - Risk Agent includes liability terms
   - Commercial Agent adds business terms
   - IP Agent defines intellectual property rights
   - Technical Agent specifies technical requirements

3. **Review & Refinement**
   - User Rights Agent ensures accessibility
   - Compliance Auditor performs checks
   - All agents validate their sections

4. **Finalization**
   - Generate final document
   - Create summary version
   - Prepare implementation checklist

### Review Workflow
1. **Document Analysis**
   - Parse existing terms
   - Identify sections and clauses
   - Extract key provisions

2. **Specialized Review**
   - Each agent reviews relevant sections
   - Identify gaps and issues
   - Generate recommendations

3. **Compliance Check**
   - Run against current regulations
   - Check industry standards
   - Verify best practices

4. **Report Generation**
   - Consolidate findings
   - Prioritize issues
   - Provide actionable recommendations

## Output Templates

### Standard Sections
1. **Definitions**
2. **Acceptance of Terms**
3. **Description of Service**
4. **User Accounts & Registration**
5. **Privacy & Data Protection**
6. **User Conduct & Prohibited Uses**
7. **Intellectual Property Rights**
8. **Payment Terms** (if applicable)
9. **Disclaimers & Limitations of Liability**
10. **Indemnification**
11. **Termination**
12. **Dispute Resolution**
13. **General Provisions**
14. **Contact Information**

### Compliance Checklist
- [ ] GDPR compliance verified
- [ ] CCPA/CPRA compliance verified
- [ ] Age verification implemented
- [ ] Cookie policy included
- [ ] Data retention defined
- [ ] User rights documented
- [ ] Breach notification procedures
- [ ] Third-party provisions
- [ ] Accessibility standards met
- [ ] Update notification process

## Configuration

```yaml
defaults:
  language: en
  jurisdiction: us
  compliance_level: standard
  accessibility_level: wcag_2.1_aa

review_settings:
  depth: comprehensive
  include_recommendations: true
  generate_summary: true
  risk_assessment: true

output_formats:
  - markdown
  - html
  - pdf
  - docx
```

## Integration Points

- **Version Control**: Git integration for tracking changes
- **Translation Services**: Multi-language support
- **Legal Database**: Access to current regulations
- **Monitoring**: Regulatory change alerts
- **Analytics**: Usage and acceptance tracking

---

*Terms of Service System v1.0 - Comprehensive legal document creation and review*