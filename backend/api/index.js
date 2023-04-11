const fs = require('fs');
const router = require('express').Router();
require('dotenv/config');

const db = require('../db');
const { getTable, multer } = require('../util/common');

router.get('/', (req, res) => {
    res.json({ module: 'API FBRO', env: process.env.NODE_ENV });
});
router.post('/insert/:tablename', async (req, res) => {
    const Model = getTable(req.params.tablename);
    try {
        const result = await db.save(Model, req.body);
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});
router.post('/insert/file/:tablename', multer.single('articleFile'), async (req, res) => {
    const Model = getTable(req.params.tablename);
    let values = {
        userId: req.body.userId,
        filename: req.file.filename,
    };
    try {
        const result = await db.save(Model, values);
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});
router.get('/get/one/:tablename', async (req, res) => {
    let Model = getTable(req.params.tablename);
    try {
        const result = await db.getOne(Model, { _id: req.body._id });
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});
router.post('/get/one/:tablename', async (req, res) => {
    let Model = getTable(req.params.tablename);
    try {
        const result = await db.getOne(Model, req.body);
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});
router.get('/get/all/:tablename', async (req, res) => {
    const Model = getTable(req.params.tablename);
    try {
        const result = await db.getAll(Model);
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});
router.post('/get/all/:tablename', async (req, res) => {
    const Model = getTable(req.params.tablename);
    try {
        const result = await db.getAll(Model, req.body);
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});
router.post('/remove/:tablename', async (req, res) => {
    const Model = getTable(req.params.tablename);
    try {
        const result = await db.removeById(Model, { _id: req.body._id });
        res.json(result);
    } catch (error) {
        console.error(error);
    }
    if (req.params.tablename == 'articleUploaded') {
        fs.unlink('./upload/' + req.body.filename, function (err) {
            if (err) throw err;
        });
    }
});
router.post('/update/relevance/query', async (req, res) => {
    const Model = getTable('query');
    try {
        const result = await db.updateRelevance(Model, {
            _id: req.body._id,
        }, { articles: req.body.articles });
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});
router.post('/update/one/:tablename', async (req, res) => {
    const Model = getTable(req.params.tablename);
    try {
        // const result = await db.updateOne(Model, { _id: req.body._id }, { relevant: req.body.relevant });
        const result = await db.updateOne(Model, { _id: req.body._id }, req.body);
        res.json(result);
        // console.log(result);
    } catch (error) {
        console.error(error);
    }
});
router.post('/update/:tablename/:id', async (req, res) => {
    const Model = getTable(req.params.tablename);
    try {
        const result = await db.updateOne(Model, { _id: req.params.id }, req.body);
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});
router.post('/login/:tablename/', async (req, res) => {
    let Model = getTable(req.params.tablename);
    try {
        const result = await db.getOne(Model, req.body);
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});
router.post('/remove/query/job', async (req, res) => {
    const Model = getTable('job');
    try {
        const result = await db.removeQuery(Model, { _id: req.body._id }, { query: req.body.query });
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});
router.post('/insert/query/job', async (req, res) => {
    const Model = getTable('job');
    try {
        const result = await db.insertQuery(Model, { _id: req.body.id }, { querys: req.body.query });
        res.json(result);
    } catch (error) {
        console.error(error);
    }
});

module.exports = router;
