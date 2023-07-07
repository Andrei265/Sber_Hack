$(function () {
	$("[data-modal]").on("click", function (event) {
		event.preventDefault();
		$(log_modal).addClass('show');
	});

	$("[data-closemodal]").on("click", function (event) {
		$(log_modal).removeClass('show');
	});

	$("[data-modalss]").on("click", function(event) {
		event.preventDefault();
		$(mini_logmodal).addClass('show1');
	});

	$("[data-closeminimodal]").on("click", function (event) {
		$(mini_logmodal).removeClass('show1');
	});
});