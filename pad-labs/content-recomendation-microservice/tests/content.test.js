const request = require('supertest');
const { describe, it, expect, afterAll } = require('@jest/globals');
const app = require('../app')

const {reqAddContent, reqUpdateContent} = require('../tests/content.test.data')

let contentId; 

describe("POST /contents", () => {
    test("should create a content", async () => {
        return request(app)
            .post("/contents")
            .send(reqAddContent)
            .expect(201)
            .then(() => {
                contentId = reqAddContent.contentId;
            })

    });
});

//get contents - sgould return all contents
describe("GET /contents", () => {
  it("should return all contents", async () => {
      return request(app)
          .get("/contents")
          .expect('Content-Type', /json/)
          .expect(200)
          .then((res) => {
              expect(res.statusCode).toBe(200);
          })
  });
});


//get content - should return a content by id
describe("GET /contents/:contentId", () => {
  it("should return a content", async () => {
    const response = await request(app)
      .get(`/contents/${contentId}`)
      .expect('Content-Type', /json/);
    expect(response.status).toBe(200);
  });
});


//update content - should update content based on id
describe("POST /contents/:contentId", () => {
  test("should create a content", async () => {
      return request(app)
          .put(`/contents/${contentId}`)
          .send(reqUpdateContent)
          .expect(201)
  });
});

//delete content - should delete a content
describe("DELETE /contents/:contentId", () => {
  test("should delete a content", async () => {
      return request(app)
          .delete(`/contents/${contentId}`)
          .expect(200)
  });
});
