import { v4 as uuidv4 } from "uuid";
import AWS from "aws-sdk";

AWS.config.update({ region: "us-east-1" });

let polly = new AWS.Polly();
let s3 = new AWS.S3();

export const handler = async (event, context) => {
  let success = true;
  let url = null;

  const pollyParams = {
    OutputFormat: "mp3",
    Text: event.text,
    VoiceId: "Matthew",
  };

  try {
    let data = await polly.synthesizeSpeech(pollyParams).promise();

    let audioStream = data.AudioStream;
    let key = uuidv4();
    let s3BucketName = "test-polly-bucket";
    let fileName = key + ".mp3";

    let uploadParams = {
      Bucket: s3BucketName,
      Key: fileName,
      Body: audioStream,
    };

    await s3.upload(uploadParams).promise();

    let signUrlParams = {
      Bucket: s3BucketName,
      Key: fileName,
    };

    url = s3.getSignedUrl("getObject", signUrlParams);
  } catch (err) {
    console.log(`Polly Error: ${err}`);

    success = false;
  }

  return {
    statusCode: 200,
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
    body: JSON.stringify({ success, url }),
  };
};
