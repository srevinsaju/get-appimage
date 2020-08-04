/*
MIT License
Copyright (c) 2020
Srevin Saju <srevinsaju (at) sugarlabs (dot) org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

var miniSearch;


function compareAlphabetically(el1, el2, index) {
  // compares el1 and el2 and returns first occurring item according
  // to ASCII
  return el1[index] == el2[index] ? 0 : (el1[index] < el2[index] ? -1 : 1);
}

function clearAppImageCards() {
  $('#activity-card-column').empty();
}

function getActivityIndex() {
  return;
}

function addAppimageCard(i, item) {
    const image_src = item['image'];
    const appimage_name = item['name'];
    const appimage_maintainer = item['maintainer'];
    const appimage_summary = item['summary'];
    const appimage_categories = item['categories_html'];
    const appimage_github = item['github'];
    const applink = item['name'].toLowerCase();
    const cardTemplate = `<div class="card appimage-card mb-medium">
      <div class="card-content">
        <div class="media">
          <div class="media-left">
            <figure class="image is-128x128">
              <img src="${image_src}" style="position:absolute; top:0; left:0; width:100%;" alt="${appimage_name} logo" loading="lazy">
            </figure>
          </div>
          <div class="media-content">
            <p class="title is-4">${appimage_name}</p>
            <p class="subtitle is-6">${appimage_maintainer}</p>
          </div>
        </div>
    
        <div class="content">
          ${appimage_summary}
          <br>
          ${appimage_categories}
        </div>
      </div>
 
      <footer class="card-footer appimage-card-footer">
        <a href="${appimage_github}" class="card-footer-item"
           target="_blank"
           rel="noreferrer">
          <i class="fa fa-github ss-i"></i><span class="ss-card-footer-text">GitHub</span>
        </a>
        <a href="../${applink}" class="card-footer-item" target="_blank"
           rel="noreferrer">
          <i class="fa fa-wifi ss-i"></i><span class="ss-card-footer-text">Website</span>
        </a>
      </footer>
    </div>`;
    $(`#col-${i%3}`).append(cardTemplate)

}


function loadAllAppImageCards() {
  // get the json file
  if ($.trim( $('#appimage-search-box').val() ) !== '') {
    // the user has entered something, filter the list accordingly
    $.getJSON('../index.min.json', function(data) {
      console.log('Searching using miniSearch');
      if (miniSearch == null) {
        // index minisearch once and only once
        // reduces CPU usage

        console.log('minisearch indexed.');
        miniSearch = new MiniSearch({
          fields: ['name', 'summary', 'maintainer'],
            // fields to index for full-text search
          storeFields: ['name', 'summary', 'maintainer', 'categories_html', 'image'],
            // fields to return with search results
          idField: 'name',
          searchOptions: {
            boost: {'name': 2},
            fuzzy: 0.5,
          },
        });
        // Index all documents
        miniSearch.addAll(data);
      }
      const results = miniSearch.search($('#appimage-search-box').val());
      $.each(results, function(i, item) {
        addAppimageCard(i, item);
      });
    });
  }
}
