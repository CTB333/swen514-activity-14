import { v4 as uuidv4 } from "uuid";
import AWS from "aws-sdk";

let polly = new AWS.Polly();
let s3 = new AWS.S3();

export const handler = async (event, context, callback) => {
  const pollyParams = {
    OutputFormat: "mp3",
    Text: event.text,
    VoiceId: "Matthew",
  };
  // 1. Getting the audio stream for the text that user entered
  polly
    .synthesizeSpeech(pollyParams)
    .on("success", function (response) {
      let data = response.data;
      let audioStream = data.AudioStream;
      let key = uuidv4();
      let s3BucketName = "test-polly-bucket";

      console.log(`Poly successfull`);

      // 2. Saving the audio stream to S3
      let params = {
        Bucket: s3BucketName,
        Key: key + ".mp3",
        Body: audioStream,
      };
      s3.putObject(params)
        .on("success", function (response) {
          console.log("S3 Successful");
        })
        .on("complete", function () {
          console.log("S3 Done");

          let s3params = {
            Bucket: s3BucketName,
            Key: key + ".mp3",
          };
          // 3. Getting a signed URL for the saved mp3 file
          let url = s3.getSignedUrl("getObject", s3params);
          // Sending the result back to the user
          let result = {
            bucket: s3BucketName,
            key: key + ".mp3",
            url: url,
          };
          callback(null, {
            statusCode: 200,
            headers: {
              "Access-Control-Allow-Origin": "*",
            },
            body: JSON.stringify(result),
          });
        })
        .on("error", function (response) {
          console.log(`S3 error: ${err}`);
        })
        .send();
    })
    .on("error", function (err) {
      console.log(`Poly error: ${err}`);

      callback(null, {
        statusCode: 500,
        headers: {
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify(err),
      });
    })
    .send();
};
