$(function () {
    let modal = $("#Modal");
    let comment_container = $("#comment_container");

    // Redirect user to login when click comment textarea
    $('.comment-form-input').on('click', function () {
        let login_url = $(this).attr('data-login-url');
        let url = $(this).attr('data-ajax-authenticator');

        $.ajax({
            url: url,
            success: function (data) {
                if (data.status == false) {
                    window.location.href = login_url;
                }
                else if (data.status== true) {
                    return
                }
            }
        });
    });

    // Redirect user to login when click reply textarea
    $('.reply-comment').on('click', function () {
        let login_url = $('.comment-form-input').attr('data-login-url');
        let url = $('.comment-form-input').attr('data-ajax-authenticator');

        $.ajax({
            url: url,
            success: function (data) {
                if (data.status == false) {
                    window.location.href = login_url;
                }
                else if (data.status== true) {
                    return
                }
            }
        });
    });

    // Redirect user to login when click like
    $('.like-button').on('click', function () {
        let login_url = $('.comment-form-input').attr('data-login-url');
        let url = $('.comment-form-input').attr('data-ajax-authenticator');

        $.ajax({
            url: url,
            success: function (data) {
                if (data.status == false) {
                    window.location.href = login_url;
                }
                else if (data.status== true) {
                    return
                }
            }
        });
    });

    function AttachEvents() {
        // comment create
        let commentForm = $("#comment-form");
        commentForm.on('submit', CreateComment);

        // comment update
        let update_comment_button = $(".js-update-comment");
        update_comment_button.on('click', ToggleModal);
        modal.on('submit', '#comment-update-form', UpdateComment);

        // comment delete
        let delete_comment_button = $(".js-delete-comment");
        delete_comment_button.on('click', DeleteComment);

        // reply create
        let reply_button = $('.js-reply-to-comment');
        reply_button.on('click', ToggleModal);
        modal.on('submit', '#reply-create-form', CreateReply);

        // reply update
        let reply_update_button = $(".js-update-reply");
        reply_update_button.on('click', ToggleModal);
        modal.on('submit', '#reply-update-form', UpdateReply);

        //reply delete
        let delete_reply_button = $(".js-delete-reply");
        delete_reply_button.on('click', DeleteReply);
    }

    // create comment
    function CreateComment(e) {
        e.preventDefault();
        let url = $(this).attr("data-url");
        let data = $(this).serialize();
        let formInput = $(this).find('.comment-form-input');
        if (formInput.val()) {
            // empty comment to escape duplicate events
            formInput.val('');

            Request(url, data, 'post').then(
                // if request successful
                function (response) {
                    // if operation successful
                    if (response['successful']) {
                        // append new comment
                        comment_container.append(response['html_content']);

                        // reattach listeners
                        AttachEvents();

                        // change counter
                        UpdateCount();
                    }
                },
                function (error) {
                    console.error('request error at CreateComment', error);
                });
        }
    }

    // update comment
    function UpdateComment(e) {
        e.preventDefault();
        let url = $(this).attr('data-url');
        let data = $(this).serialize();

        $(this).find('.form-input').val(''); // empty the text area to stop from resubmit

        Request(url, data, 'post').then(
            // if request successful
            function (response) {
                // if operation successful
                if (response['successful']) {
                    modal['foundation']('close');
                    let comment = $(`#comment_${response['pk']}`); // get the you want comment
                    comment.replaceWith(response['html_content']); // replace comment with updated version

                    // reattach listeners
                    AttachEvents();
                }
            },
            function (error) {
                console.log("error in func: UpdateComment, file: Comment.js", error)
            }
        );
    }

    // delete comment
    function DeleteComment(e) {
        e.preventDefault();
        let url = $(this).attr('data-url');
        Request(url, null, 'get').then(
            // if request successful
            function (response) {
                // if operation successful
                if (response['successful']) {
                    let comment = $(`#comment_${response['pk']}`);
                    // remove the comment replies container from page
                    comment.siblings(`.reply-container_${response['pk']}`).remove();
                    // remove comment from page
                    comment.remove();

                    // change counter
                    UpdateCount();
                } else {
                    console.error(response['message']);
                }
            },
            function (error) {
                console.error("request error at DeleteComment", error);
            }
        );
    }

    // create comment
    function CreateReply(e) {
        e.preventDefault();
        let url = $(this).attr('data-url');
        let data = $(this).serialize();
        let formInput = $(this).find('.form-input');

        if (formInput.val()) {

            formInput.val(''); // empty reply input to avoid duplicated events

            Request(url, data, 'post').then(
                function (response) {
                    let reply_container = $(".reply-container_" + response['pk']);
                    reply_container.append(response['html_content']);
                    modal['foundation']('close');

                    // reattach listeners
                    AttachEvents();

                    // change counter
                    UpdateCount();
                },
                function (error) {
                    console.error("request error in func: CreateReply, file: Comment.js", error);
                });
        }
    }

    // update reply
    function UpdateReply(e) {
        e.preventDefault();
        let url = $(this).attr('data-url');
        let data = $(this).serialize();

        $(this).find('.form-input').val('');

        Request(url, data, 'post').then(
            function (response) {
                if (response['successful']) {
                    modal['foundation']('close');
                    let reply = $(`#reply_${response['pk']}`);
                    reply.replaceWith(response['html_content']);

                    // reattach listeners
                    AttachEvents();
                } else {
                    modal.html(response['message'])
                }
            },
            function (error) {
                console.error("error in func: UpdateReply, file: Comment.js", error)
            })
    }

    // delete reply
    function DeleteReply(e) {
        e.preventDefault();
        let url = $(this).attr('data-url');

        Request(url, null, 'get').then(
            // if request successful
            function (response) {
                if (response['successful']) {
                    let reply = $("#reply_" + response['pk']);
                    reply.remove();

                    // change counter
                    UpdateCount();
                } else {
                    // log operation error
                    console.error(response['message'])
                }
            }, function (error) {
                console.error("request error at func: DeleteReply, file: Comment.js", error);
            })
    }

    //  opens a modal with a form
    function ToggleModal(e) {
        e.preventDefault();
        let url = $(this).attr('data-url');

        Request(url, null, 'get').then(
            // if request successful
            function (response) {
                // if operation successful
                if (response['successful']) {
                    modal.foundation("open");
                    modal.html(response['html_form']);
                }
            },
            function (error) {
                console.error('request error in func: ToggleModal, file: Comment.js', error);
            },
        );
    }

    // ajax request used on all event handlers
    function Request(url = null, data = null, method = 'post') {
        return $.ajax({
            "url": url,
            "type": method, // request type
            "dataType": "json", // expected data type
            "data": data,
        });
    }

    // Comment Counter
    function UpdateCount() {
        let comments = $(".comment");
        let forLoop = 0;
        // count comments
        for (let comment of comments) {
            forLoop++;
        }
        let comment_counter = $('#comment_counter');
        // reset to zero
        if (forLoop < 0) {
            forLoop = 0;
        }
        // update comment counter
        comment_counter.html(`Comments ${forLoop}`);
    }

    AttachEvents();
});