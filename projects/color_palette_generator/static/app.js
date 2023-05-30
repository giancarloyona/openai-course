const form = document.querySelector("#form");

form.addEventListener("submit", function (e) {
    e.preventDefault();
    get_colors();
});

function get_colors() {
    const query = form.elements.query.value;
    fetch("/palette", {
        method: "POST",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            query: query,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            const colors = data.colors;
            const container = document.querySelector(".container");
            create_color_boxes(colors, container);
        });
}

function create_color_boxes(colors, parent) {
    parent.innerHTML = "";

    for (const color of colors) {
        const div = document.createElement("div");

        div.style.backgroundColor = color;
        div.style.width = `calc(100%/${colors.length})`;
        div.classList.add("color");

        div.addEventListener("click", function () {
            navigator.clipboard.writeText(color);
        });

        const span = document.createElement("span");
        span.innerText = color;
        div.appendChild(span);

        parent.appendChild(div);
    }
}
