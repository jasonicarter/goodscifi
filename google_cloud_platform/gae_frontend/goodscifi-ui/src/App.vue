<!--
Inspired by Jecelyn Yeen
https://github.com/chybie/file-upload-vue
https://scotch.io/tutorials/how-to-handle-file-uploads-in-vue-2
-->

<!-- HTML Template -->
<template>
  <div id="app" class="container">

    <div id="header-row" class="row">
      <div class="twelve columns">
        <h1>GOOD SCI-FI</h1>
        Judging books by their covers since July 1st, 2017</br>
        <span class="disclaimer">Good Sci-Fi is a machine learning, science fiction,
          book cover image classifier.</br>
        Open-sourced and openly discussed, personal project on
        <a href="https://github.com/jasonicarter">Github</a> and
        <a href="https://medium.com/towards-data-science/4-months-of-machine-deep-learning-89f6ab56a2fd">
          Medium.</a></span>
      </div>
    </div>

    <div id="prediction-row" class="row">
      <!-- UPLOAD -->
      <div class="one-third column center-content">
        <form class="prediction-results center-content" enctype="multipart/form-data" novalidate>
          <div class="dropbox center-content">
            <input type="file" multiple :disabled="isSaving"
              @change="fileChange($event.target.files);
              "accept="image/*" class="input-file">

              <div class='dropbox-message'>
                <p v-if="isInitial || isSuccess">
                  Drag your file here<br>or click to browser
                </p>
                <p v-if="isSaving">
                  Judging a book by it's cover...
                </p>
                <p v-if="isFailed">
                  Upload has failed<br>Please check your file and try again
                  <pre>{{ uploadError }}</pre>
                </p>
              </div>
          </div>
        </form>
      </div>

      <!-- SUCCESS -->
      <div class="one-third column center-content">
        <div class="prediction-results center-content ">
          <div class="probability">
            <img v-if="isSuccess" :src="uploadedImage.url"
                 class="img-left img-thumbnail" :alt="uploadedImage.fileName">
             <p v-if="isInitial || isSaving">
               AI Stuff<br>...Happens
             </p>
           </div>
        </div>
      </div>

      <!-- PROBABILITY -->
      <div class="one-third column center-content">
        <div class="prediction-results center-content ">
              <div class="probability">
                <span v-if="isSuccess" class="prob">{{ uploadedImage.probability }}%</span>
                <p v-if="isInitial || isSaving">
                  Good Sci-Fi</br>...???
                </p>
              </div>
        </div>
      </div>
    </div>

   </div>
</template>


<!-- JavaScript -->
<script>
  import * as axios from 'axios';

  const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;

  export default {
    name: 'app',
    data() {
      return {
        uploadedFiles: [],
        uploadedImage: {},
        uploadError: null,
        currentStatus: null,
        result: {}
      }
    },
    computed: {
      isInitial() {
        return this.currentStatus === STATUS_INITIAL;
      },
      isSaving() {
        return this.currentStatus === STATUS_SAVING;
      },
      isSuccess() {
        return this.currentStatus === STATUS_SUCCESS;
      },
      isFailed() {
        return this.currentStatus === STATUS_FAILED;
      }
    },
    methods: {
      reset() {
        // reset form to initial state
        this.currentStatus = STATUS_INITIAL;
        this.uploadedFiles = [];
        this.uploadError = null;
      },
      fileChange(files) {
        // reset after error message or upload attempted
        this.reset();
        if (!files.length) return;

        // save it - only one file accepted
        this.save(files[0]);
      },
      save(file) {
        this.currentStatus = STATUS_SAVING;

        // TODO: google storage / datastore save data
        this.get_predictions(file)
      },
      get_predictions(file) {
          // const BASE_URL = 'http://localhost:5000';
          const BASE_URL = 'http://api.goodscifi.com/api/v1';
          const url = `${BASE_URL}/books`;
          const fReader = new FileReader();

          console.log(file)

          fReader.onload = () => {
              var img_url = fReader.result
              var img_base64 = JSON.stringify(img_url.replace(/^data:image\/[a-z]+;base64,/, ""));
              var json_data = {data: img_base64};

              var config = {
                headers: {'Content-Type': 'application/json'}
              }

              return axios.post(url, json_data, config)
                  // get response
                  .then(x => x.data['predictions'])
                  .then(x =>
                      x.map(img =>
                        Object.assign({}, img,
                          {probability: Math.floor(img.probability)},
                          {url: img_url})
                      )
                  )
                  .then(x => {
                    this.uploadedFiles = [].concat(x[0]); //TODO: remove index
                    this.uploadedImage = x[0];
                    this.currentStatus = STATUS_SUCCESS;
                    console.log(x)
                  })
                  .catch(err => {
                    this.uploadError = err.response;
                    this.currentStatus = STATUS_FAILED;
                  });
          }

          fReader.readAsDataURL(file);
      }
    },
    mounted() {
      this.reset();
    },
  }

</script>


<!-- Styling -->
<style lang="css">
  #header-row {
    margin-top: 10%;
    text-align: center;
  }
  #prediction-row {
    margin-top: 2%;
    margin-bottom: 2%;
    text-align: center;
  }

  .dropbox {
    outline-offset: -5px;
    background: whitesmoke;
    color: dimgray;
    padding: 10px 10px;
    max-width: 170px;
    max-height: 220px;
    position: relative;
    cursor: pointer;
    border-radius: 5px;
  }
  .dropbox-message {
    display: inline-block;
    font-weight: lighter;
    margin: 40px 20px;
  }
  .dropbox:hover {
    background: lightgrey;
    height: 200px;
  }
  .dropbox p {
    font-size: 1em;
  }

  .input-file {
    opacity: 0;
    width: 100%;
    height: 220px;
    position: absolute;
    cursor: pointer;
  }

  .img-left {
    float: left;
    padding: 1px;
    background-color: darkgrey;
    margin-right: 5px;
  }
  .img-thumbnail {
    width: 170px;
    height: 220px;
    margin: 0;
    object-fit: cover;
  }

  .probability {
    font-weight: lighter;
    color: dimgray;
  }
  .probability span {
    font-size: 3em;
    font-weight: lighter;
  }
  .probability-box {
    width: 170px;
    height: 200px;
    background-color: whitesmoke
  }

  .list-unstyled {
    list-style: none;
    padding: 0px;
  }

  .center-content {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .prediction-results {
    width: 170px;
    height: 220px;
    background-color: whitesmoke;
    border-radius: 5px;
    margin-bottom: 5%;
  }
  .prediction-results span.prob {
    font-size: 5em;
  }

  .disclaimer{
    color: grey;
    font-size: 1.3rem;
  }

</style>
