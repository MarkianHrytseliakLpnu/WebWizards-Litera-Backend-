$(document).ready(function() {
    console.log("✅ Автодоповнення підключено");

    $("#searchInput").autocomplete({
        source: function(request, response) {
            console.log("🔍 Надсилаємо запит: " + request.term);
            $.ajax({
                url: autocompleteUrl,  // Використовуємо змінну з book.html
                data: { q: request.term },
                dataType: "json",
                success: function(data) {
                    console.log("📌 Отримані дані:", data);
                    response(data);
                },
                error: function(xhr, status, error) {
                    console.error("❌ Помилка запиту:", status, error);
                }
            });
        },
        minLength: 1,
        select: function(event, ui) {
            $("#searchInput").val(ui.item.value);
            $("#searchForm").submit();
        }
    });
});