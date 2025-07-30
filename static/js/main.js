// Getting header's elements
const header = document.querySelector('header');
const nav = document.querySelector('nav');
const header_img = document.querySelector('.header-img');
header_img.style.height = header.offsetHeight - nav.offsetHeight + 'px';

// Resizing header
addEventListener("resize", (event) => {
	header.style.height = '100vh';
	header_img.style.height = header.offsetHeight - nav.offsetHeight + 'px';
})
