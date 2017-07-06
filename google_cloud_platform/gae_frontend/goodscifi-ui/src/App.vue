<!--
Borrowed from Jecelyn Yeen
https://github.com/chybie/file-upload-vue
https://scotch.io/tutorials/how-to-handle-file-uploads-in-vue-2
-->

<!-- HTML Template -->
<template>
  <div id="app">
    <div class="container">
      <!-- Upload -->
      <form enctype="multipart/form-data" novalidate v-if="isInitial || isSaving">
        <h1>Good Sci-Fi AI</h1>
        <span>Judging books by their cover since July 1st, 2017</span>
        <div class="dropbox">
          <input type="file" :name="uploadFileName" :disabled="isSaving"
            @change="filesChange($event.target.name, $event.target.files);
            " accept="image/*" class="input-file">

            <p v-if="isInitial">
              Drag your file here to begin<br> or click to browser
            </p>
            <p v-if="isSaving">
              Judging a book by it's cover...
            </p>

            <!-- <img src="" height="200" alt="Image preview..."> -->

        </div>
      </form>

      <!--SUCCESS-->
       <div v-if="isSuccess">
         <h2>Uploaded {{ uploadedFiles.length }} file(s) successfully.</h2>
         <p>
           <a href="javascript:void(0)" @click="reset()">Upload again</a>
         </p>
         <ul class="list-unstyled">
           <li v-for="item in uploadedFiles">
             <p>{{ item.description }} {{ item.probability }}</p>
             <img :src="item.url" class="img-responsive img-thumbnail" :alt="item.fileName">
           </li>
         </ul>
       </div>

       <!--FAILED-->
       <div v-if="isFailed">
         <h2>Uploaded failed.</h2>
         <p>
           <a href="javascript:void(0)" @click="reset()">Try again</a>
         </p>
         <pre>{{ uploadError }}</pre>
       </div>
     </div>
   </div>
</template>


<!-- JavaScript -->
<script>
  // swap as you need
  import { wait } from './utils';
  // import { upload } from './file-upload.fake.service';
  import * as axios from 'axios';

  const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;

  export default {
    name: 'app',
    data() {
      return {
        uploadedFiles: [],
        uploadError: null,
        currentStatus: null,
        uploadFileName: 'photos',
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
      save(formData) {
        // upload data to the server
        this.currentStatus = STATUS_SAVING;
        // TODO: google storage / datastore save data

        this.get_predictions(formData)
      },
      filesChange(fieldName, fileList) {
        // handle file changes
        const formData = new FormData();

        if (!fileList.length) return;

        // append the files to FormData
        Array
          .from(Array(fileList.length).keys())
          .map(x => {
            formData.append(fieldName, fileList[x], fileList[x].name);
          });

        // save it
        this.save(formData);
      },
      get_predictions(formData) {
          const BASE_URL = 'http://localhost:5000';
          const file = formData.get('photos');
          const url = `${BASE_URL}`;
          const fReader = new FileReader();

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
                        Object.assign({}, img, {url: img_url})
                      )
                  )
                  .then(x => {
                    this.uploadedFiles = [].concat(x);
                    this.currentStatus = STATUS_SUCCESS;
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
  .dropbox {
    outline: 1px dashed grey;
    outline-offset: -5px;
    background: whitesmoke;
    color: dimgray;
    padding: 10px 10px;
    min-height: 200px; /* minimum height */
    position: relative;
    cursor: pointer;
  }

  .input-file {
    opacity: 0;
    width: 100%;
    height: 200px;
    position: absolute;
    cursor: pointer;
  }

  .dropbox:hover {
    background: lightgrey;
  }

  .dropbox p {
    font-size: 1.2em;
    text-align: center;
    padding: 50px 0;
  }
</style>
