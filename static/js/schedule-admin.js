// Getting schedules block and all schedules
let schedules_block = document.querySelector('.schedules');
let schedules = document.querySelectorAll('.schedule');

function move_up(event) {
    let schedule = event.currentTarget.schedule;
    // Updating previous schedule's position
    let schedule_prev = document.querySelector('.pos-' + (Number(schedule.className.split(" ")[1].split('-')[1]) - 1));
    console.log('.pos-' + (Number(schedule.className.split(" ")[1].split('-')[1]) - 1));
    let schedule_prev_position = schedule_prev.querySelector('.schedule-position');
    schedule_prev_position.setAttribute('value', Number(schedule_prev.className.split(' ')[1].split('-')[1]) + 1);
    schedule_prev.className = 'schedule pos-' + (Number(schedule_prev.className.split(' ')[1].split('-')[1]) + 1);

    // Updating schedule's position
    let schedule_position = schedule.querySelector('.schedule-position');
    schedule_position.setAttribute('value', Number(schedule.className.split(' ')[1].split('-')[1]) - 1);
    schedule.className = 'schedule pos-' + (Number(schedule.className.split(' ')[1].split('-')[1]) - 1);

    // Moving the schedule
    schedule.remove();
    schedule_prev.insertAdjacentHTML('beforebegin', schedule.outerHTML);

    // Processing schedule's buttons
    schedule_buttons();
}

function move_down(event) {
    let schedule = event.currentTarget.schedule;
    // Updating next schedule's position
    let schedule_next = document.querySelector('.pos-'+ (Number(schedule.className.split(" ")[1].split('-')[1]) + 1));
    let schedule_next_position = schedule_next.querySelector('.schedule-position');
    schedule_next_position.setAttribute('value', Number(schedule_next.className.split(' ')[1].split('-')[1]) - 1);
    schedule_next.className = 'schedule pos-' + (Number(schedule_next.className.split(' ')[1].split('-')[1]) - 1);

    // Updating schedule's position
    let schedule_position = schedule.querySelector('.schedule-position');
    schedule_position.setAttribute('value', Number(schedule.className.split(' ')[1].split('-')[1]) + 1);
    schedule.className = 'schedule pos-' + (Number(schedule.className.split(' ')[1].split('-')[1]) + 1);

    // Moving the schedule
    schedule.remove();
    schedule_next.insertAdjacentHTML('afterend', schedule.outerHTML);

    // Processing schedule's buttons
    schedule_buttons();
}

// Processing schedules
function schedule_buttons() {
    schedules = document.querySelectorAll('.schedule');
    for (let i = 0; i < schedules.length; i++) {
        // Getting schedule's buttons
        const schedule = schedules[i];
        let schedule_move_up = schedule.querySelector('.schedule-move-up');
        let schedule_move_down = schedule.querySelector('.schedule-move-down');
        let schedule_delete = schedule.querySelector('.schedule-delete');
        // Processing valid buttons
        if (i == 0) {
            schedule_move_up.style.display = 'none';
        } else {
            schedule_move_up.style.display = 'block';
        }
        if (i == schedules.length - 1) {
            schedule_move_down.style.display = 'none';
        } else {
            schedule_move_down.style.display = 'block';
        }

        // 'Move up' button
        schedule_move_up.removeEventListener('click', move_up);
        schedule_move_up.addEventListener('click', move_up);
        schedule_move_up.schedule = schedule;

        // 'Move down' button
        schedule_move_down.removeEventListener('click', move_down);
        schedule_move_down.addEventListener('click', move_down);
        schedule_move_down.schedule = schedule;
    }
}

for (let i = 0; i < schedules.length; i++) {
        // Getting schedule's buttons
        const schedule = schedules[i];
        let schedule_delete = schedule.querySelector('.schedule-delete');

        // 'Delete schedule' button
        schedule_delete.addEventListener('click', (event) => {
            let schedule_is_deleted = schedule.querySelector('.schedule-is-deleted');
            schedule_is_deleted.setAttribute('value', '1');
            schedule.style.display = 'none';
        });

        // Opening schedule for a view
        let schedule_img = schedule.querySelector('.schedule-img');
        schedule_img.addEventListener('click', (event) => {
            schedules_block.insertAdjacentHTML('beforeend', `<div class="schedule-active">
                                                                    ${schedule_img.outerHTML}
                                                                    <div class="schedule-bg"></div>
                                                                </div>`);
            let schedule_active = document.querySelector('.schedule-active');
            let schedule_bg = schedule_active.querySelector('.schedule-bg');
            schedule_bg.addEventListener('click', (event) => {
                schedule_active.remove();
            });
        });
    }

schedule_buttons();
