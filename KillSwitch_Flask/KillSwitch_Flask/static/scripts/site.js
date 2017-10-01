var ruleStatusUrl = "/ruleStatus";

$(function () {
    $("input:checkbox").on("change", function () {
        var ruleCheckbox = $(this);
        var id = ruleCheckbox.data("ruleId");
        var ruleName = ruleCheckbox.data("ruleName");
        var newStatus = ruleCheckbox.context.checked ? '' : 'True'; // Python only considers '' as false. Also this was reversed for user presentation. 
        var data = { "ruleId": id, "active": newStatus };
        $.post(ruleStatusUrl, data)
            .done(function (data) {
                if (true == data.success && '' == newStatus) {
                    ruleCheckbox.closest("div").removeClass("inactive");
                    ruleCheckbox.closest("div").addClass("active");
                    ruleCheckbox.closest("li").data("sort-string", "0-" + ruleName);
                } else {
                    ruleCheckbox.closest("div").removeClass("active");
                    ruleCheckbox.closest("div").addClass("inactive");
                    ruleCheckbox.closest("li").data("sort-string", "1-" + ruleName);
                }
                sortRules();
            });
    });
    sortRules();
});

function sortRules() {
    var rules = $('ul.js-rules'),
        rulesLi = rules.children('li');
    rulesLi.sort(function (a, b) {
        var an = $(a).data('sort-string'),
            bn = $(b).data('sort-string');
        if (an > bn) 
            return 1;
        if (an < bn) 
            return -1;
        return 0;
    });
    rulesLi.detach().appendTo(rules);
}