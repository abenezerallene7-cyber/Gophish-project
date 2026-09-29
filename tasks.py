from app import celery
from models import db, Scan, Finding
from scanner import run_scan
from ai_advisor import enrich_findings

@celery.task(bind=True)
def scan_target(self, user_id, target):
    self.update_state(state='PROGRESS', meta={'status': 'Running scan modules...'})

    try:
        findings, risk_score, risk_level = run_scan(target)
        findings = enrich_findings(findings)

        scan = Scan(
            user_id=user_id,
            target=target,
            risk_score=risk_score,
            risk_level=risk_level,
            status='completed'
        )
        db.session.add(scan)
        db.session.flush()

        for f in findings:
            finding = Finding(
                scan_id=scan.id,
                issue_name=f['issue_name'],
                severity=f['severity'],
                description=f.get('description', ''),
                recommendation=f.get('recommendation', ''),
                category=f.get('category', 'general')
            )
            db.session.add(finding)
        db.session.commit()

        return {'scan_id': scan.id, 'risk_score': risk_score, 'risk_level': risk_level}
    except Exception as e:
        # Log error and mark scan as failed (if we created one)
        scan = Scan(
            user_id=user_id,
            target=target,
            risk_score=0,
            risk_level='Failed',
            status='failed'
        )
        db.session.add(scan)
        db.session.commit()
        return {'error': str(e)}