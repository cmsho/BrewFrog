const beersPerColumn = 3;
const beersPerPage = 3;

var currentPage = 1;


// Create cards for beers in favorites list
function buildCards(beers) {
    $('#cards').empty();
    if (beers.length != 0) {
        for (var i = 0; i < beers.length; i++) {
            let beer = beers[i];
            let card = $('<div>').addClass('card')
                .append(
                    $('<img>').addClass('card-img-top').attr('src', '/img/beer/' + beer.image)
                ).append(
                    $('<p>').addClass('card-body')
                        .append(
                            $('<h5>').addClass('card-title').text(beer.name)
                        ).append(
                            $('<p>').addClass('card-text').text(beer.brewery)
                        ).append(
                            $('<p>').addClass('card-text').text('Style: ' + beer.style)
                        ).append(
                            $('<p>').addClass('card-text').text('ABV: ' + beer.abv)
                        ).append(
                            $('<p>').addClass('card-text').text('IBUs: ' + beer.ibu)
                        ).append(
                            $('<p>').addClass('card-text').text('Calories: ' + beer.calories)
                        ).append(
                            $('<a>').addClass('btn btn-primary').text('Unfavorite')
                                .click(function () {
                                    unfavoriteBeer(beer.uid);
                                })
                        )
                );
    
            if (i % beersPerColumn == 0)
                $('#cards').append(
                    $('<div>').addClass('card-deck')
                );
            $('#cards .card-deck').last().append(card);
        }
        while ($('#cards .card-deck:last .card').length < beersPerColumn)
            $('#cards .card-deck').last().append($('<div>').addClass('card'));
    }
 
    else{
        $('#cards').append(
            $('<p>').addClass('alert d-flex justify-content-center').text('No favorites found! \n Go favorite some beers!')
        )
    }
}

// Pagination
function createPageLink(text, toPage, active, disabled) {
    
    let link = $('<li>').addClass('page-item').append(
        $('<a>').addClass('page-link').text(text).click(function () {
            currentPage = toPage;
            loadBeers();
        })
    );
    if (active)
        link.addClass('active');
    if (disabled)
        link.addClass('disabled');
    return link;
}

function updatePagination(total) {
    if (total != 0){
        let pages = Math.ceil(total / beersPerPage);
        $('#paginator').empty().append(
            createPageLink('Previous', currentPage - 1, false, currentPage == 1)
        );
        for (var page = 1; page <= pages; page++)
            $('#paginator').append(
                createPageLink(page, page, page == currentPage, false)
            );
        $('#paginator').append(
            createPageLink('Next', currentPage + 1, false, currentPage == pages)
        );
    }
}

function updatePage(data) {
    buildCards(data.beer);
    updatePagination(data.total);
}

// Load favorites
function loadBeers() {
    $.get("api/my_favorites", {        
        n: beersPerPage,
        offset: (currentPage - 1) * beersPerPage
    }, function (data) {
        updatePage(data);
    });
}

// Remove a favorite
function unfavoriteBeer(uid) {
    $.get("api/unfavorite", {
        uid: uid,
        n: beersPerPage,
        offset: (currentPage - 1) * beersPerPage
    }, function (data) {
        updatePage(data);
    });
}

// Init favorites list when page loads
$(function () {
    loadBeers();
});
