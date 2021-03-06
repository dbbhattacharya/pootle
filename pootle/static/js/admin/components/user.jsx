/*
 * Copyright (C) Pootle contributors.
 *
 * This file is a part of the Pootle project. It is distributed under the GPL3
 * or later license. See the LICENSE file for a copy of the license and the
 * AUTHORS file for copyright and authorship information.
 */

'use strict';

var React = require('react');

var Search = require('./search');
var UserForm = require('forms').UserForm;
var models = require('models/user');


var UsersAdmin = React.createClass({

  render: function () {
    var viewsMap = {
      add: <UserAdd
              model={this.props.model}
              collection={this.props.items}
              handleSuccess={this.props.handleSave}
              handleCancel={this.props.handleCancel} />,
      edit: <UserEdit
              model={this.props.selectedItem}
              collection={this.props.items}
              handleAdd={this.props.handleAdd}
              handleSuccess={this.props.handleSave}
              handleDelete={this.props.handleDelete} />
    };

    var args = {
      count: this.props.items.count,
    }, msg;

    if (this.props.searchQuery) {
      msg = ngettext('%(count)s user matches your query.',
                     '%(count)s users match your query.', args.count);
    } else {
      msg = ngettext(
        'There is %(count)s user.',
        'There are %(count)s users. Below are the most recently added ones.',
        args.count
      );
    }
    var resultsCaption = interpolate(msg, args, true);

    var fields = ['index', 'full_name', 'username', 'email'];

    return (
      <div className="admin-app-users">
        <div className="module first">
          <Search
            fields={fields}
            handleSearch={this.props.handleSearch}
            handleSelectItem={this.props.handleSelectItem}
            items={this.props.items}
            selectedItem={this.props.selectedItem}
            searchLabel={gettext('Search Users')}
            searchPlaceholder={gettext('Find user by name, email, properties')}
            resultsCaption={resultsCaption}
            searchQuery={this.props.searchQuery} />
        </div>

        <div className="module admin-content">
          {viewsMap[this.props.view]}
        </div>
      </div>
    );
  }

});


var UserAdd = React.createClass({

  /* Layout */

  render: function () {
    return (
      <div className="item-add">
        <div className="hd">
          <h2>{gettext('Add User')}</h2>
          <button
            onClick={this.props.handleCancel}
            className="btn btn-primary">{gettext('Cancel')}</button>
        </div>
        <div className="bd">
          <UserForm
            model={new this.props.model()}
            collection={this.props.collection}
            handleSuccess={this.props.handleSuccess} />
        </div>
      </div>
    );
  }

});


var UserEdit = React.createClass({

  /* Layout */

  render: function () {
    return (
      <div className="item-edit">
        <div className="hd">
          <h2>{gettext('Edit User')}</h2>
          <button
            onClick={this.props.handleAdd}
            className="btn btn-primary">{gettext('Add User')}</button>
        </div>
        <div className="bd">
        {!this.props.model ?
          <p>{gettext('Use the search form to find the user, then click on a user to edit.')}</p> :
          <UserForm
            key={this.props.model.id}
            model={this.props.model}
            collection={this.props.collection}
            handleSuccess={this.props.handleSuccess}
            handleDelete={this.props.handleDelete} />
        }
        </div>
      </div>
    );
  }

});


module.exports = {
  App: UsersAdmin,
  model: models.User,
  collection: models.UserSet,
};
