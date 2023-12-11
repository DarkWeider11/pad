var express = require('express');
const Content = require('../model/contentModel');
const router = express.Router();

//CRUD operations for content
router.post('/contents', async (req, res) => {
    const {contentId, title, rating, genre, cast, release_year } = req.body;
  
    try {
        // checking if the content with the same contentId already exists
        const existingContent = await Content.findOne({ contentId });

        if (existingContent) {
            return res.status(400).json({ error: 'Content with the same contentId already exists.' });
        }
        const content = new Content({
            contentId,
            title,
            rating,
            genre, 
            cast,
            release_year 
        });
        await content.save();
        return res.status(201).json({ message: 'Content added succesfully.' });
    } catch (error) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

router.get('/contents', async (req, res) => {
    try {
        const contents = await Content.find();
        res.status(200).json(contents)
    } catch (error) {
        res.status(404).json({message: error.message});
    }
})

router.get('/contents/:contentId', async (req, res) => {
    const contentId = req.params;
    // console.log(`Content ID: ${contentId}`);

    try {
        const content = await Content.findOne(contentId);

        if (!content) {
            return res.status(404).json({ error: 'Content not found' });
        }

        return res.status(200).json(content);
    } catch (error) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

router.put('/contents/:contentId', async (req, res) => {
    const contentId = req.params.contentId;
    const { title, rating, genre, cast, release_year } = req.body;

    try {
        let content = await Content.findOne({ contentId });

        if (!content) {
            return res.status(404).json({ error: 'Content not found' });
        }

        content.title = title || content.title;
        content.rating = rating || content.rating;
        content.genre = genre || content.genre;
        content.cast = cast || content.cast;
        content.release_year = release_year || content.release_year;

        await content.save();

        return res.status(201).json({ message: 'Content updated successfully.' });
    } catch (error) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

router.delete('/contents/:contentId', async (req, res) => {
    const contentId = req.params.contentId;
    // console.log(`Content ID: ${contentId}`);

    try {
        const content = await Content.findOne({contentId});

        if (!content) {
            return res.status(404).json({ error: 'Content not found' });
        }

        await content.deleteOne();

        return res.status(200).json({ message: 'Content deleted successfully.' });
    } catch (error) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});


module.exports = router;