// Getting all coaches and theirs images and infos
const coaches = document.querySelectorAll('.coach');
const coaches_img = document.querySelectorAll('.coach-img');
const coaches_info = document.querySelectorAll('.coach-info');

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
if (window.innerWidth <= 950) {
	for (let i = 0; i < coaches.length; i++) {
		coaches[i].style.height = coaches_img[i].offsetHeight + coaches_info[i].offsetHeight + 35 + 'px';
		coaches_img[i].style.height = 400 + 'px';
	}
} else if (window.innerWidth <= 1350) {
	for (let i = 0; i < coaches.length; i++) {
        if (Number(coaches_info[i].offsetHeight) + 70 < 700) {
            coaches[i].style.height = 700 + 'px';
            coaches_img[i].style.height = 630 + 'px';
        } else {
            coaches[i].style.height = coaches_info[i].offsetHeight + 70 + 'px';
            coaches_img[i].style.height = coaches_info[i].offsetHeight + 'px';
        }
	}
} else {
	for (let i = 0; i < coaches.length; i++) {
		if (Number(coaches_info[i].offsetHeight) + 70 < 600) {
            coaches[i].style.height = 600 + 'px';
            coaches_img[i].style.height = 530 + 'px';
        } else {
            coaches[i].style.height = coaches_info[i].offsetHeight + 70 + 'px';
            coaches_img[i].style.height = coaches_info[i].offsetHeight + 'px';
        }
	}
};

addEventListener("resize", (event) => {
	if (window.innerWidth <= 950) {
        for (let i = 0; i < coaches.length; i++) {
            coaches[i].style.height = coaches_img[i].offsetHeight + coaches_info[i].offsetHeight + 35 + 'px';
            coaches_img[i].style.height = 400 + 'px';
        }
    } else if (window.innerWidth <= 1350) {
        for (let i = 0; i < coaches.length; i++) {
            if (Number(coaches_info[i].offsetHeight) + 70 < 700) {
                coaches[i].style.height = 700 + 'px';
                coaches_img[i].style.height = 630 + 'px';
            } else {
                coaches[i].style.height = coaches_info[i].offsetHeight + 70 + 'px';
                coaches_img[i].style.height = coaches_info[i].offsetHeight + 'px';
            }
        }
    } else {
        for (let i = 0; i < coaches.length; i++) {
            if (Number(coaches_info[i].offsetHeight) + 70 < 600) {
                coaches[i].style.height = 600 + 'px';
                coaches_img[i].style.height = 530 + 'px';
            } else {
                coaches[i].style.height = coaches_info[i].offsetHeight + 70 + 'px';
                coaches_img[i].style.height = coaches_info[i].offsetHeight + 'px';
            }
        }
    };
})