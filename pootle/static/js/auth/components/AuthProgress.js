/*
 * Copyright (C) Pootle contributors.
 *
 * This file is a part of the Pootle project. It is distributed under the GPL3
 * or later license. See the LICENSE file for a copy of the license and the
 * AUTHORS file for copyright and authorship information.
 */

'use strict';

import React from 'react';
import { PureRenderMixin } from 'react/addons';


let AuthProgress = React.createClass({
  mixins: [PureRenderMixin],

  propTypes: {
    msg: React.PropTypes.string.isRequired,
  },

  render() {
    // FIXME: use flexbox when possible
    let style = {
      outer: {
        display: 'table',
        height: '20em',
        width: '100%',
        textAlign: 'center',
      },
      inner: {
        display: 'table-cell',
        verticalAlign: 'middle',
      },
    };

    return (
      <div style={style.outer}>
        <div style={style.inner}>
          <p>{this.props.msg}</p>
        </div>
      </div>
    );
  },

});


export default AuthProgress;
