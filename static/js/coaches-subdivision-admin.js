// Getting all coaches and theirs images and infos
let coaches = document.querySelectorAll('.coach');
let coaches_img = document.querySelectorAll('.coach-img');
let coaches_info = document.querySelectorAll('.coach-info');

// Adding coaches' image
for (let i = 0; i < coaches_img.length; i++) {
    // Adding coach's image if it has valid format
    if (['png', 'jpg', 'jpeg'].includes(coaches_img[i].className.split(' ')[2])) {
        coaches_img[i].style.background = "url('../static/images/coaches/" + coaches_img[i].className.split(' ')[1] + "." + coaches_img[i].className.split(' ')[2] + "')";
        coaches_img[i].style.backgroundSize = "cover";
        coaches_img[i].style.backgroundPosition = "center";
    // Adding coach's image placeholder otherwise
    } else {
        coaches_img[i].style.background = "url('../static/images/coaches/0.jpg')";
        coaches_img[i].style.backgroundSize = "cover";
        coaches_img[i].style.backgroundPosition = "center";
    };
};

// Resizing coaches' divs
const resizeObserver = new ResizeObserver((entries) => {
    for (const entry in entries) {
        if (window.innerWidth <= 950) {
            for (let i = 0; i < coaches.length; i++) {
                coaches[i].style.height = coaches_img[i].offsetHeight + coaches_info[i].offsetHeight + 35 + 'px';
            }
        } else if (window.innerWidth <= 1350) {
            for (let i = 0; i < coaches.length; i++) {
                if (Number(coaches_info[i].offsetHeight) + 70 < 700) {
                    coaches[i].style.height = 700 + 'px';
                } else {
                    coaches[i].style.height = coaches_info[i].offsetHeight + 70 + 'px';
                }
            }
        } else {
            for (let i = 0; i < coaches.length; i++) {
                if (Number(coaches_info[i].offsetHeight) + 70 < 600) {
                    coaches[i].style.height = 600 + 'px';
                } else {
                    coaches[i].style.height = coaches_info[i].offsetHeight + 70 + 'px';
                }
            }
        };
    }
})

// Processing coaches' infos
for (let i = 0; i < coaches_info.length; i++) {
    coaches_info[i].style.width = coaches[i].offsetWidth - coaches_img[i].offsetWidth - 70 + 'px';
    resizeObserver.observe(coaches_info[i])

    // 'Add new list' button
    let coach_buttons_add_list = coaches_info[i].querySelector('.coach-info-add-list');
    coach_buttons_add_list.addEventListener('click', (event) => {
        coach_buttons_add_list.insertAdjacentHTML('beforebegin', `<div class="coach-info-ul">
                                                                    <ul class="coach-info-list">
                                                                        <li class="coach-info-list-item">
                                                                            <textarea name="coach_list_item ${coaches_info[i].querySelectorAll('.coach-info-list').length}"><Заголовок></textarea>
                                                                        </li>
                                                                    </ul>
                                                                    <div class="coach-info-buttons">
                                                                        <div class="coach-info-add-list-item">Добавить поле</div>
                                                                        <div class="coach-info-delete-list-item">Удалить поле</div>
                                                                        <div class="coach-info-delete-list">Удалить блок</div>
                                                                    </div>
                                                                </div>`);
        // Adding new 'Add new list item' button
        coach_info_lists = coaches[i].querySelectorAll('.coach-info-ul');
        const coach_info_list = coach_info_lists[coach_info_lists.length - 1]
        const coach_info_list_num = coach_info_lists.length - 1
        const coach_info_list_add_item = coach_info_list.querySelector('.coach-info-add-list-item');
        const coach_info_list_ul = coach_info_list.querySelector('ul');
        coach_info_list_add_item.addEventListener('click', (event) => {
            coach_info_list_ul.insertAdjacentHTML('beforeend', `<li class="coach-info-list-item">
                                                                    <textarea name="coach_list_item ${coach_info_list_num}"></textarea>
                                                                </li>`);
            coach_info_list_lis = coach_info_list.querySelectorAll('li');
        });
        // Adding new 'Delete list item' button
        const coach_info_list_delete_item = coach_info_list.querySelector('.coach-info-delete-list-item');
        let coach_info_list_lis = coach_info_list.querySelectorAll('li');
        coach_info_list_delete_item.addEventListener('click', (event) => {
           coach_info_list_lis[coach_info_list_lis.length - 1].remove()
           coach_info_list_lis = coach_info_list.querySelectorAll('li');
           if (coach_info_list_lis.length == 0) {
                coach_info_list.remove()
           }
        });
        // Adding new 'Delete list' button
        const coach_info_delete_list = coach_info_list.querySelector('.coach-info-delete-list');
        coach_info_delete_list.addEventListener('click', (event) => {
            coach_info_list.remove()
            coach_info_lists = coaches[i].querySelectorAll('.coach-info-ul');
        });
    });

    // Processing coach's lists' buttons
    let coach_info_lists = coaches[i].querySelectorAll('.coach-info-ul');
    for (let j = 0; j < coach_info_lists.length; j++) {
        // 'Add new list item' button
        const coach_info_list_add_item = coach_info_lists[j].querySelector('.coach-info-add-list-item');
        const coach_info_list_ul = coach_info_lists[j].querySelector('ul');
        coach_info_list_add_item.addEventListener('click', (event) => {
           coach_info_list_ul.insertAdjacentHTML('beforeend', `<li class="coach-info-list-item">
                                                                    <textarea name="coach_list_item ${j}"></textarea>
                                                                </li>`);
           coach_info_list_lis = coach_info_lists[j].querySelectorAll('li');
        });

        // 'Delete list item' button
        const coach_info_list_delete_item = coach_info_lists[j].querySelector('.coach-info-delete-list-item');
        let coach_info_list_lis = coach_info_lists[j].querySelectorAll('li');
        coach_info_list_delete_item.addEventListener('click', (event) => {
           coach_info_list_lis[coach_info_list_lis.length - 1].remove()
           coach_info_list_lis = coach_info_lists[j].querySelectorAll('li');
           if (coach_info_list_lis.length == 0) {
                coach_info_lists[j].remove()
           }
        });

        // 'Delete list' button
        const coach_info_delete_list = coach_info_lists[j].querySelector('.coach-info-delete-list');
        coach_info_delete_list.addEventListener('click', (event) => {
            coach_info_lists[j].remove()
        });
    }

    // 'Delete coach' button
    const coach_delete = coaches[i].querySelector('.coach-delete');
    const coach_is_deleted = coaches[i].querySelector('.coach-is-deleted');
    coach_delete.addEventListener('click', (event) => {
        coach_is_deleted.setAttribute('value', '1');
        coaches[i].submit();
    });
};

// 'Add new coach' button
const coaches_add = document.querySelector('.coaches-add');
coaches_add.addEventListener('click', (event) => {
    coaches_add.insertAdjacentHTML('beforebegin', `<form action="/coaches-${window.location.href.split('-admin')[0].split('-')[1]}-admin" method="post" enctype="multipart/form-data" class="coach">
                                                        <input type="hidden" name="coach_is_deleted" value="0" class="coach-is-deleted">
                                                        <input type="hidden" name="coach_id" value="-1">
                                                        <input type="hidden" name="coach_subdivision" value="${window.location.href.split('-admin')[0].split('-')[1]}">
                                                        <div class="coach-img -1 None"></div>
                                                        <div class="coach-info">
                                                            <textarea class="coach-info-title" name="coach_name">Имя тренера</textarea>
                                                            <div class="coach-info-ul">
                                                                <ul class="coach-info-list">
                                                                    <li class="coach-info-list-item">
                                                                        <textarea name="coach_list_item 0"><Достижения></textarea>
                                                                    </li>
                                                                </ul>
                                                                <div class="coach-info-buttons">
                                                                    <div class="coach-info-add-list-item">Добавить поле</div>
                                                                    <div class="coach-info-delete-list-item">Удалить поле</div>
                                                                    <div class="coach-info-delete-list">Удалить блок</div>
                                                                </div>
                                                            </div>
                                                            <div class="coach-info-ul">
                                                                <ul class="coach-info-list">
                                                                    <li class="coach-info-list-item">
                                                                        <textarea name="coach_list_item 1"><Направления работы></textarea>
                                                                    </li>
                                                                </ul>
                                                                <div class="coach-info-buttons">
                                                                    <div class="coach-info-add-list-item">Добавить поле</div>
                                                                    <div class="coach-info-delete-list-item">Удалить поле</div>
                                                                    <div class="coach-info-delete-list">Удалить блок</div>
                                                                </div>
                                                            </div>
                                                            <div class="coach-info-add-list">Добавить блок</div>
                                                            <div>
                                                                <div class="coach-info-phone">
                                                                    Телефон для связи: <textarea name="coach_phone">+8 (846-35) 3-58-51</textarea>
                                                                </div>
                                                                <div class="coach-info-address">
                                                                    <textarea name="coach_address">ФСК «Олимп» (ул. Миронова, д. 32 «А»)</textarea>
                                                                </div>
                                                            </div>
                                                            <div class="coach-info-buttons">
                                                                <input type="file" accept="image/png, image/jpeg, image/jpg" name="coach_img">
                                                                <input type="submit" value="Сохранить">
                                                                <div class="coach-delete">Удалить тренера</div>
                                                            </div>
                                                        </div>
                                                    </form>`);
    // Updating coaches variables
    coaches = document.querySelectorAll('.coach');
    coaches_img = document.querySelectorAll('.coach-img');
    coaches_info = document.querySelectorAll('.coach-info');
    // Processing new coach elements
    const coach = coaches[coaches.length - 1]
    const coach_img = coaches_img[coaches_img.length - 1]
    const coach_info = coaches_info[coaches_info.length - 1]
    // Adding placeholder to new coach's image
    coach_img.style.background = "url('../static/images/coaches/0.jpg')";
    coach_img.style.backgroundSize = "cover";
    coach_img.style.backgroundPosition = "center";
    // Processing coach's lists
    let coach_info_lists = coach.querySelectorAll('.coach-info-ul');
    // 'Add new list' button
    const coach_buttons_add_list = coach.querySelector('.coach-info-add-list');
    coach_buttons_add_list.addEventListener('click', (event) => {
        coach_buttons_add_list.insertAdjacentHTML('beforebegin', `<div class="coach-info-ul">
                                                                    <ul class="coach-info-list">
                                                                        <li class="coach-info-list-item">
                                                                            <textarea name="coach_list_item ${coach_info.querySelectorAll('.coach-info-list').length}"><Заголовок></textarea>
                                                                        </li>
                                                                    </ul>
                                                                    <div class="coach-info-buttons">
                                                                        <div class="coach-info-add-list-item">Добавить поле</div>
                                                                        <div class="coach-info-delete-list-item">Удалить поле</div>
                                                                        <div class="coach-info-delete-list">Удалить блок</div>
                                                                    </div>
                                                                </div>`);
        // Adding new 'Add new list item' button
        coach_info_lists = coach.querySelectorAll('.coach-info-ul');
        const coach_info_list = coach_info_lists[coach_info_lists.length - 1]
        const coach_info_list_num = coach_info_lists.length - 1
        const coach_info_list_add_item = coach_info_list.querySelector('.coach-info-add-list-item');
        const coach_info_list_ul = coach_info_list.querySelector('ul');
        coach_info_list_add_item.addEventListener('click', (event) => {
            coach_info_list_ul.insertAdjacentHTML('beforeend', `<li class="coach-info-list-item">
                                                                    <textarea name="coach_list_item ${coach_info_list_num}"></textarea>
                                                                </li>`);
            coach_info_list_lis = coach_info_list.querySelectorAll('li');
        });
        // Adding new 'Delete list item' button
        const coach_info_list_delete_item = coach_info_list.querySelector('.coach-info-delete-list-item');
        let coach_info_list_lis = coach_info_list.querySelectorAll('li');
        coach_info_list_delete_item.addEventListener('click', (event) => {
           coach_info_list_lis[coach_info_list_lis.length - 1].remove()
           coach_info_list_lis = coach_info_list.querySelectorAll('li');
           if (coach_info_list_lis.length == 0) {
                coach_info_list.remove()
           }
        });
        // Adding new 'Delete list' button
        const coach_info_delete_list = coach_info_list.querySelector('.coach-info-delete-list');
        coach_info_delete_list.addEventListener('click', (event) => {
            coach_info_list.remove()
            coach_info_lists = coaches[i].querySelectorAll('.coach-info-ul');
        });
    });
    for (let j = 0; j < coach_info_lists.length; j++) {
        // 'Add new list item' button
        const coach_info_list_add_item = coach_info_lists[j].querySelector('.coach-info-add-list-item');
        const coach_info_list_ul = coach_info_lists[j].querySelector('ul');
        coach_info_list_add_item.addEventListener('click', (event) => {
           coach_info_list_ul.insertAdjacentHTML('beforeend', `<li class="coach-info-list-item">
                                                                    <textarea name="coach_list_item ${j}"></textarea>
                                                                </li>`);
           coach_info_list_lis = coach_info_lists[j].querySelectorAll('li');
        });

        // 'Delete list item' button
        const coach_info_list_delete_item = coach_info_lists[j].querySelector('.coach-info-delete-list-item');
        let coach_info_list_lis = coach_info_lists[j].querySelectorAll('li');
        coach_info_list_delete_item.addEventListener('click', (event) => {
           coach_info_list_lis[coach_info_list_lis.length - 1].remove()
           coach_info_list_lis = coach_info_lists[j].querySelectorAll('li');
           if (coach_info_list_lis.length == 0) {
                coach_info_lists[j].remove()
           }
        });

        // 'Delete list' button
        const coach_info_delete_list = coach_info_lists[j].querySelector('.coach-info-delete-list');
        coach_info_delete_list.addEventListener('click', (event) => {
            coach_info_lists[j].remove()
        });
    }

    // 'Delete coach' button
    const coach_delete = coach.querySelector('.coach-delete');
    const coach_is_deleted = coach.querySelector('.coach-is-deleted');
    coach_delete.addEventListener('click', (event) => {
        coach_is_deleted.setAttribute('value', '1');
        coach.submit();
    });

    resizeObserver.observe(coach_info)
    coach_info.style.width = coach.offsetWidth - coach_img.offsetWidth - 70 + 'px';
});

// Resizing coaches' divs
if (window.innerWidth <= 950) {
	for (let i = 0; i < coaches.length; i++) {
		coaches[i].style.height = coaches_img[i].offsetHeight + coaches_info[i].offsetHeight + 35 + 'px';
	}
} else if (window.innerWidth <= 1350) {
	for (let i = 0; i < coaches.length; i++) {
        if (Number(coaches_info[i].offsetHeight) + 70 < 700) {
            coaches[i].style.height = 700 + 'px';
        } else {
            coaches[i].style.height = coaches_info[i].offsetHeight + 70 + 'px';
        }
	}
} else {
	for (let i = 0; i < coaches.length; i++) {
		if (Number(coaches_info[i].offsetHeight) + 70 < 600) {
            coaches[i].style.height = 600 + 'px';
        } else {
            coaches[i].style.height = coaches_info[i].offsetHeight + 70 + 'px';
        }
	}
};

addEventListener("resize", (event) => {
    for (let i = 0; i < coaches_info.length; i++) {
        coaches_info[i].style.width = coaches[i].offsetWidth - coaches_img[i].offsetWidth - 70 + 'px';
    };

	if (window.innerWidth <= 950) {
        for (let i = 0; i < coaches.length; i++) {
            coaches[i].style.height = coaches_img[i].offsetHeight + coaches_info[i].offsetHeight + 35 + 'px';
        }
    } else if (window.innerWidth <= 1350) {
        for (let i = 0; i < coaches.length; i++) {
            if (Number(coaches_info[i].offsetHeight) + 70 < 700) {
                coaches[i].style.height = 700 + 'px';
            } else {
                coaches[i].style.height = coaches_info[i].offsetHeight + 70 + 'px';
            }
        }
    } else {
        for (let i = 0; i < coaches.length; i++) {
            if (Number(coaches_info[i].offsetHeight) + 70 < 600) {
                coaches[i].style.height = 600 + 'px';
            } else {
                coaches[i].style.height = coaches_info[i].offsetHeight + 70 + 'px';
            }
        }
    };
})