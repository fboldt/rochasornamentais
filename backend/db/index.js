module.exports = {
    getAll: async (Model, filter = {}) => {
        return await Model.find(filter);
    },
    getOne: async (Model, filter) => {
        return await Model.findOne(filter);
    },
    save: async (Model, value) => {
        return await new Model(value).save();
    },
    removeById: async (Model, value) => {
        return await Model.findOneAndDelete(value);
    },
    updateOne: async (Model, filter, update) => {
        return await Model.findOneAndUpdate(filter, update);
    },
    removeQuery: async (Model, filter, value) => {
        return await Model.findOneAndUpdate(filter, {
            $pull: { querys: { $in: value.query } }
        });
    },
    insertQuery: async (Model, filter, value) => {
        return await Model.findOneAndUpdate(filter, {
            $push: { querys: value.querys }
        });
    },
    updateRelevance: async (Model, filter, value) => {
        return await Model.findOneAndUpdate(filter, {
            $set: value,
        });
    },
};
