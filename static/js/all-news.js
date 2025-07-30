// Getting news' images
let news_img = document.querySelectorAll('.news-img');
for (let i = 0; i < news_img.length; i++) {
    // Adding new's image if it has valid format
    if (['png', 'jpg', 'jpeg'].includes(news_img[i].className.split(' ')[2])) {
        news_img[i].style.background = "url('../static/images/news/" + news_img[i].className.split(' ')[1] + "." + news_img[i].className.split(' ')[2] + "')";
        news_img[i].style.backgroundSize = "cover";
        news_img[i].style.backgroundPosition = "center";
    // Adding new's image placeholder otherwise
    } else {
        news_img[i].style.background = "url('../static/images/news/0.jpg')";
        news_img[i].style.backgroundSize = "cover";
        news_img[i].style.backgroundPosition = "center";
    };
};

// Getting more news from server when screen is scrolled to the end
const news_block = document.querySelector('.news-block');
posts_offset = 1;
window_height = null;
let flag = true;
window.addEventListener('scroll', function() {
// Getting html objects
    let body = document.body;
    let html = document.documentElement;
    let height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
    if (window_height == height) {
        return false;
    }
    // Checking screen position
    if (height - window.scrollY < html.clientHeight * 2 && flag) {
        window_height = height;
        // Getting data from server
        let server_url = window.location.href + '/add-posts-' + (++posts_offset).toString();
        fetch(server_url)
        .then(res => res.json())
        .then(function(res) {
            news_block.insertAdjacentHTML('beforeend', res[0]);
            flag = res[1];
            news_img = document.querySelectorAll('.news-img');
            for (let i = 0; i < news_img.length; i++) {
                // Adding new's image if it has valid format
                if (['png', 'jpg', 'jpeg'].includes(news_img[i].className.split(' ')[2])) {
                    news_img[i].style.background = "url('../static/images/news/" + news_img[i].className.split(' ')[1] + "." + news_img[i].className.split(' ')[2] + "')";
                    news_img[i].style.backgroundSize = "cover";
                    news_img[i].style.backgroundPosition = "center";
                // Adding new's image placeholder otherwise
                } else {
                    news_img[i].style.background = "url('../static/images/news/0.jpg')";
                    news_img[i].style.backgroundSize = "cover";
                    news_img[i].style.backgroundPosition = "center";
                };
            };
        })
    }
});