let allImages = [];
let activeCategory = null;
let categoryButtons = {};

const categoriesFile = "categories_rules.json";
const imagesFile = "images.json";

const categorySortPatterns = {
  "Messier": /\bm\s*-?\s*(\d{1,3})\b/i,
  "Caldwell": /\bc\s*-?\s*(\d{1,3})\b/i,
  "NGC": /\bngc\s*-?\s*(\d{1,4})\b/i,
  "IC": /\bic\s*-?\s*(\d{1,4})\b/i,
  "Sharpless": /\b(?:sh|sh1|sh2|sharpless)\s*-?\s*(\d{1,3})\b/i,
  "Lynds LdN": /\bl(?:dn|nd)\s*[_-]?\s*(\d{1,4})\b/i,
  "Abell": /\babell\s*(\d{1,4})\b/i,
  "Arp": /\barp\s*(\d{1,3})\b/i
};


// ctrl + shift + r  to for deeper refresh

const gallery = document.getElementById("gallery");
const categoryBar = document.getElementById("category-bar");


// Load categories
fetch(categoriesFile)
  .then(res => res.json())
  .then(data => {
    data.categories.forEach(cat => {
      const name = cat.name;

      const btn = document.createElement("button");
      btn.innerHTML = name.replace(" ", "<br>");
      btn.classList.add("category-button");

      btn.addEventListener("click", () => {
        activeCategory = name;
        updateGallery();
        setActiveButton(btn);
      });

      categoryBar.appendChild(btn);

      // store reference
      categoryButtons[name] = btn;
    });

    // Optional "All" button
    const allBtn = document.createElement("button");
    allBtn.textContent = "All";
    allBtn.classList.add("category-button", "active");

    allBtn.addEventListener("click", () => {
      activeCategory = null;
      updateGallery();
      setActiveButton(allBtn);
    });

    categoryBar.prepend(allBtn);
  });

// Load images
fetch(imagesFile)
  .then(res => res.json())
  .then(data => {
    allImages = Array.isArray(data) ? data : data.images || [];

    updateCategoryCounts(); // 👈 add this
    updateGallery();
  });

function getSortKey(fileName, category) {

  // no active category or no special sort rule
  if (!category || !categorySortPatterns.hasOwnProperty(category)) {
    return fileName;
  }

  const pattern = categorySortPatterns[category];

  if (!pattern) {
    return fileName;
  }

  const match = fileName.match(pattern);

  // category exists but filename doesn't contain that catalog
  if (!match || !match[1]) {
    return fileName;
  }

  return Number(match[1]);
}


function compareImages(a, b) {

  const keyA = getSortKey(a.file, activeCategory);
  const keyB = getSortKey(b.file, activeCategory);

  // both catalog numbers found
  if (
    typeof keyA === "number" &&
    typeof keyB === "number"
  ) {
    return keyA - keyB;
  }

  // fallback
  return a.file.localeCompare(
    b.file,
    undefined,
    {
      numeric: true,
      sensitivity: "base"
    }
  );
}

function formatSharpless(value) {

  if (!value) return null;

  // Extract number from "Sharpless 125"
  const match = value.match(/(\d+)/);

  if (!match) return null;

  const num = match[1];

  return `Sh 2-${num}`;
}

function resolvePrimaryObject(item) {

  const ids = item?.info?.identifiers;

  if (!ids) return null;

  const priority = ["NGC", "IC", "Messier", "Sharpless"];

  for (const key of priority) {

    if (!ids[key]) continue;

    let value = ids[key];

    // Normalize Sharpless for CDS
    if (key === "Sharpless") {
      value = formatSharpless(value);
    }

    return {
      type: key,
      value: value,
      raw: ids[key]
    };
  }

  return null;
}

function openImageViewer(item) {

  const file = item.file;
  const name = getDisplayName(file);

  const object = resolvePrimaryObject(item);

  const cdsUrl = object
    ? `https://cdsportal.u-strasbg.fr/?target=${encodeURIComponent(object.value)}`
    : "https://cdsportal.u-strasbg.fr/";

  const imageUrl =
    "images/" +
    encodeURIComponent(file);

  const metaHtml = buildInfoHtml(item);

  const viewer = window.open("", "_blank");

  if (!viewer) return;


  viewer.document.write(`

    <html>

      <head>
        <title>${name}</title>
        <link rel="stylesheet" href="style.css">
      </head>

      <body class="viewer-body">

        <div class="viewer-container">


          <div class="viewer-image-panel">

            <a href="${cdsUrl}" target="_blank">
              <img src="${imageUrl}" alt="${name}">
            </a>

          </div>


          <div class="viewer-info-panel">

            <div class="viewer-meta-block">
              ${metaHtml}
            </div>

            <div class="viewer-extra-block">
              Future CDS / links / tools here
            </div>

          </div>


        </div>

      </body>

    </html>

  `);

  viewer.document.close();
}

function createImageContainer(item) {

  const file = item.file;
  const name = getDisplayName(file);

  const container =
    document.createElement("div");

  container.classList.add(
    "image-container"
  );


  const label =
    document.createElement("div");

  label.classList.add(
    "image-label"
  );

  label.textContent = name;


  const link = document.createElement("a");

  link.href = "#";


  link.addEventListener("click", (e) => {
    e.preventDefault();
    openImageViewer(item);
  });

  const img =
    document.createElement("img");

  img.src =
    "images/" +
    encodeURIComponent(file);

  img.alt = name;

  link.appendChild(img);


  const info =
    createInfoElements(item);


  container.appendChild(
    info.button
  );

  container.appendChild(
    info.box
  );

  container.appendChild(
    label
  );

  container.appendChild(
    link
  );

  return container;
}


function createInfoElements(item) {

  const infoBtn =
    document.createElement("button");

  infoBtn.textContent = "i";
  infoBtn.classList.add("info-btn");


  const infoBox =
    document.createElement("div");

  infoBox.classList.add("info-box");
  infoBox.style.display = "none";

  infoBtn.addEventListener(
    "click",
    (e) => {

      e.preventDefault();
      e.stopPropagation();

      // populate dynamically
      infoBox.innerHTML =
        buildInfoHtml(item);

      infoBox.style.display =
        infoBox.style.display === "none"
          ? "block"
          : "none";
    }
  );

  return {
    button: infoBtn,
    box: infoBox
  };
}

function buildInfoHtml(item) {

  if (!item.info) {
    return "No information";
  }

  const info = item.info;

  let html = "";

  if (info.title) {
    html += `<div>${info.title}</div>`;
  }

  if (info.designation) {
    html += `<div>${info.designation}</div>`;
  }

  if (info.type) {
    html += `<div>${info.type}</div>`;
  }

  if (info.distance) {
    html += `<div>${info.distance}</div>`;
  }

  // NEW: identifiers block
  if (info.identifiers) {

    html += `<div>Identifiers</div>`;
    
    html += `<div class="identifiers-list">`;

    for (const [catalog, value] of Object.entries(info.identifiers)) {
      html += `<div>${catalog}: ${value}</div>`;
    }
    html += `</div>`;
  }

  // NEW: extended_info block
  if (info.extended_info) {

    html += `<div>Extended Info</div>`;
    html += `<div class="extended-info-list">`;

    for (const [key, value] of Object.entries(info.extended_info)) {
      html += `<div>${key}: ${value}</div>`;
    }

    html += `</div>`;
  }

  return html || "No information";
}

function getDisplayName(fileName) {

  const lastDot =
    fileName.lastIndexOf(".");

  return fileName.substring(
    0,
    lastDot
  );
}

function getFilteredImages() {

  if (!activeCategory) {
    return allImages;
  }

  return allImages.filter(img =>
    img.categories.some(
      c => c.trim() === activeCategory
    )
  );
}


// Update gallery display
function updateGallery() {

  gallery.innerHTML = "";

  const filtered = getFilteredImages();

  filtered.sort(compareImages);

  filtered.forEach(item => {
    gallery.appendChild(
      createImageContainer(item)
    );
  });
}

// Highlight active button
function setActiveButton(activeBtn) {
  document.querySelectorAll(".category-button").forEach(btn =>
    btn.classList.remove("active")
  );
  activeBtn.classList.add("active");
}

function updateCategoryCounts() {
  const uncategorizedCount = allImages.filter(img =>
    img.categories.includes("Uncategorized")
  ).length;

  const btn = categoryButtons["Uncategorized"];

  if (btn) {
    if (uncategorizedCount > 0) {
      btn.innerHTML = `Uncategorized<br>(${uncategorizedCount})`;
    } else {
      btn.innerHTML = "Uncategorized";
    }
  }
}