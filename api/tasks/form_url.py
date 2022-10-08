from api.control.models import WeekID
from api.form_url.models import ResultsFormURL
from api.rus.models import Essay
from api.services import filter_objects
from triproverochki.celery import app


@app.task
def create_result_form_urls_for_essay_authors():
    current_week_id = WeekID.get_current()
    for essay in filter_objects(
        Essay.objects, task__week_id=current_week_id, only=('author',)
    ):
        ResultsFormURL.objects.create(user=essay.author, week_id=current_week_id)
