let news_img = document.querySelector('.news-img');
// Adding coach's image if it has valid format
if (['png', 'jpg', 'jpeg'].includes(news_img.className.split(' ')[2])) {
    news_img.style.background = "url('../static/images/news/" + news_img.className.split(' ')[1] + "." + news_img.className.split(' ')[2] + "')";
    news_img.style.backgroundSize = "cover";
    news_img.style.backgroundPosition = "center";
// Adding coach's image placeholder otherwise
} else {
    news_img.style.background = "url('../static/images/news/0.jpg')";
    news_img.style.backgroundSize = "cover";
    news_img.style.backgroundPosition = "center";
};